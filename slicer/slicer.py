import numpy as np
from scipy.io import wavfile
import label_reader.label_reader_interface as lri
import label_reader.audacity_label_reader as alr
import os


class DataSlicer:

    def __init__(self, audio_file_path):
        self.audio_file_path = audio_file_path
        if os.path.isfile(self.audio_file_path):
            self.audio_sample_rate, self.data = wavfile.read(audio_file_path)
            self.audio_samples_length = len(self.data)
            self.audio_file_duration_seconds = self.audio_samples_length / self.audio_sample_rate
        elif self.audio_file_path is not None:
            raise FileNotFoundError

    def slice_by_samples(self, start, end) -> []:
        if start >= 0 and end < self.audio_samples_length:
            return self.data[start:end]
        else:
            raise Exception("Invalid start or end argument!")

    def slice_by_seconds(self, start, end) -> []:
        start_samples = int(start * self.audio_sample_rate)
        end_samples = int(end * self.audio_sample_rate)
        return self.slice_by_samples(start_samples, end_samples)


class DataWriter:

    def __init__(self, audio_file_path,
                 output_folder_path,
                 file_prefix: str = "slice_",
                 sample_rate=44100):
        self.output_folder_path = output_folder_path
        self.data_slicer = DataSlicer(audio_file_path)
        self.file_prefix = file_prefix
        self.sample_rate = sample_rate
        if os.path.isdir(self.output_folder_path):
            pass
        else:
            os.mkdir(self.output_folder_path)
            #raise Exception("Invalid output folder!")

    def write_to_file(self, data, file_suffix: str = "_1_30"):
        file_name = self.file_prefix + file_suffix + ".wav"
        file_path = self.output_folder_path + "/" + file_name
        wavfile.write(file_path, self.sample_rate, data.astype(np.int16))
        print("Created " + file_path + " file.")


class Slicer:

    def __init__(self, txt_label_file_path,
                 audio_file_path,
                 output_folder_path,
                 data_padding=True,
                 output_file_length_seconds=2,
                 output_file_prefix: str = "slice_",
                 label_value_filer: list = None):
        self.txt_label_file_path = txt_label_file_path
        self.audio_file_path = audio_file_path
        self.output_folder_path = output_folder_path
        self.data_padding = data_padding
        self.output_file_prefix = output_file_prefix
        self.output_file_length_seconds = output_file_length_seconds
        self.label_value_filer = label_value_filer

        self.label_reader = alr.AudacityLabelReader(txt_label_file_path=self.txt_label_file_path,
                                                    audio_file_path=self.audio_file_path)
        self.data_slicer = DataSlicer(self.audio_file_path)
        self.data_writer = DataWriter(audio_file_path=self.audio_file_path,
                                      output_folder_path=self.output_folder_path,
                                      sample_rate=self.data_slicer.audio_sample_rate,
                                      file_prefix=self.output_file_prefix)

    def export_all(self):
        labels = self.label_reader.get_labels_seconds(limit_to_audio_length=True)
        for label in labels:
            start_of_label = float(label[lri.LABEL_READER_INTERFACE_START_OF_LABEL_SECONDS])
            end_of_label = float(label[lri.LABEL_READER_INTERFACE_END_OF_LABEL_SECONDS])
            label_value = label[lri.LABEL_READER_INTERFACE_VALUE]
            is_label_valid = True
            if self.label_value_filer is not None:
                is_label_valid = False
                for filter_value in self.label_value_filer:
                    if filter_value == label_value:
                        is_label_valid = True

            if is_label_valid:
                start_of_label_seconds = int(start_of_label)
                start_of_label_minutes = 0
                if start_of_label > 60:
                    start_of_label_minutes = int(start_of_label/60)
                    start_of_label_seconds = int(start_of_label - start_of_label_minutes * 60)
                file_suffix = label_value + "_" + str(start_of_label_minutes) + "_" + str(start_of_label_seconds)
                data_slice = self.data_slicer.slice_by_seconds(start_of_label, end_of_label)
                if self.data_padding:

                    data_length_samples = len(data_slice)
                    expected_data_length_samples = self.data_slicer.audio_sample_rate * self.output_file_length_seconds
                    need_to_be_added_samples = expected_data_length_samples - data_length_samples
                    need_to_be_added_to_front_samples = 0
                    need_to_be_added_to_tail_samples = 0

                    new_data_slice = np.zeros((expected_data_length_samples, 2))

                    if need_to_be_added_samples > 0:

                        if (need_to_be_added_samples % 2) == 0:
                            #Number is even
                            need_to_be_added_to_front_samples = int(need_to_be_added_samples/2)
                            need_to_be_added_to_tail_samples = int(need_to_be_added_samples/2)
                        else:
                            #Number is odd
                            need_to_be_added_samples -= 1
                            need_to_be_added_to_front_samples = int(need_to_be_added_samples / 2)
                            need_to_be_added_to_tail_samples = int((need_to_be_added_samples / 2)) + 1

                        # Copy data_slice array to the center of the new_data_slice
                        for i in range(0, len(data_slice)):
                            new_data_slice[i + need_to_be_added_to_front_samples - 1, 0] = data_slice[i, 0]
                            new_data_slice[i + need_to_be_added_to_front_samples - 1, 1] = data_slice[i, 1]

                        data_slice = new_data_slice
                    else:
                        # TODO: handle a case where slice if bigger than expected file size
                        pass

                self.data_writer.write_to_file(data_slice, file_suffix=file_suffix)

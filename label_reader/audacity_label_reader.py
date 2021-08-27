import label_reader.label_reader_interface as I
import numpy as np
from scipy.io import wavfile
import os


class AudacityLabelReader(I.LabelReaderInterface):

    def __init__(self, txt_label_file_path=None, audio_file_path=None):
        self.txt_label_file_path = txt_label_file_path
        self.audio_file_path = audio_file_path
        self.audio_file_duration_seconds = 0
        "Read txt file and returns labels dataframe"
        if os.path.isfile(self.txt_label_file_path):
            with open(txt_label_file_path) as f:
                self.labels = f.read()
                if self.labels.find("\\\t", 0, 50) > 0:
                    self.labels = [l.split('\t') for l in self.labels.split('\n')][:-1]
                    self.labels = [l for o in self.labels for l in o]
                    self.labels = [l for l in self.labels]
                    self.labels = [l for l in self.labels if l != '\\']
                    self.labels = np.array(self.labels).reshape(-1, 5)
                else:
                    self.labels = [l.split('\t') for l in self.labels.split('\n')][:-1]
        elif self.txt_label_file_path is not None:
            raise FileNotFoundError

        if os.path.isfile(self.audio_file_path):
            self.audio_sample_rate, self.data = wavfile.read(audio_file_path)
            self.audio_samples_length = len(self.data)
            self.audio_file_duration_seconds = self.audio_samples_length / self.audio_sample_rate
        elif self.audio_file_path is not None:
            raise FileNotFoundError

    def get_labels_seconds(self, limit_to_audio_length=False) -> dict:
        labels_seconds_list = list()
        for label in self.labels:
            label_length = len(label)
            low_frequency = 0
            high_frequency = 0
            if label_length > 3:
                low_frequency = label[3]
                high_frequency = label[4]

            end_of_label_seconds = float(label[1])
            if limit_to_audio_length and self.audio_file_duration_seconds != 0:
                if end_of_label_seconds > self.audio_file_duration_seconds:
                    return labels_seconds_list
            labels_seconds_list.append({I.LABEL_READER_INTERFACE_START_OF_LABEL_SECONDS: label[0],
                                   I.LABEL_READER_INTERFACE_END_OF_LABEL_SECONDS: end_of_label_seconds,
                                   I.LABEL_READER_INTERFACE_VALUE: label[2],
                                   I.LABEL_READER_INTERFACE_LOW_FREQUENCY_OF_LABEL_SECONDS: low_frequency,
                                   I.LABEL_READER_INTERFACE_HIGH_FREQUENCY_OF_LABEL_SECONDS: high_frequency})
        return labels_seconds_list

    def get_labels_samples(self, limit_to_audio_length=False) -> dict:
        labels_samples_list = list()
        seconds_per_sample = 1/self.audio_sample_rate
        for label in self.labels:
            label_length = len(label)
            low_frequency = 0
            high_frequency = 0
            if label_length > 3:
                low_frequency = label[3]
                high_frequency = label[4]
            start_of_label_samples = float(label[0])/seconds_per_sample
            end_of_label_samples = float(label[1])/seconds_per_sample
            if limit_to_audio_length and self.audio_file_duration_seconds != 0:
                if end_of_label_samples > self.audio_samples_length - 1:
                    return labels_samples_list
            labels_samples_list.append({I.LABEL_READER_INTERFACE_START_OF_LABEL_SECONDS: start_of_label_samples,
                                        I.LABEL_READER_INTERFACE_END_OF_LABEL_SECONDS: end_of_label_samples,
                                        I.LABEL_READER_INTERFACE_VALUE: label[2],
                                        I.LABEL_READER_INTERFACE_LOW_FREQUENCY_OF_LABEL_SECONDS: low_frequency,
                                        I.LABEL_READER_INTERFACE_HIGH_FREQUENCY_OF_LABEL_SECONDS: high_frequency})
        return labels_samples_list
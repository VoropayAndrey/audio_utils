from slicer.slicer import Slicer

AUDACITY_LABEL_TXT_FILE_PATH = "data/ReferenceLabels.txt"
AUDACITY_AUDIO_FILE_PATH = "data/Reference.wav"
AUDACITY_OUTPUT_FOLDER_PATH = "data/output"

def test_slicer_1():
    slicer = Slicer(txt_label_file_path=AUDACITY_LABEL_TXT_FILE_PATH,
                    audio_file_path=AUDACITY_AUDIO_FILE_PATH,
                    output_folder_path=AUDACITY_OUTPUT_FOLDER_PATH)
    slicer.export_all()

if __name__ == '__main__':
    test_slicer_1()
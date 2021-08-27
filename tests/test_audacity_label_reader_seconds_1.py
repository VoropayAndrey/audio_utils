from label_reader.audacity_label_reader import AudacityLabelReader

AUDACITY_LABEL_TXT_FILE_PATH = "data/ReferenceLabels.txt"
AUDACITY_AUDIO_FILE_PATH = "data/Reference.wav"


def test_seconds_1():
    alr = AudacityLabelReader(AUDACITY_LABEL_TXT_FILE_PATH, AUDACITY_AUDIO_FILE_PATH)
    labels_dict = alr.get_labels_seconds()
    assert(len(labels_dict) > 0)


def test_seconds_2():
    alr = AudacityLabelReader(AUDACITY_LABEL_TXT_FILE_PATH, AUDACITY_AUDIO_FILE_PATH)
    labels_dict = alr.get_labels_seconds(limit_to_audio_length=True)
    assert (len(labels_dict) > 0)
    assert (len(labels_dict) <= 290)


if __name__ == '__main__':
    test_seconds_2()
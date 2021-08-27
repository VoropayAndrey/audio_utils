import abc

LABEL_READER_INTERFACE_START_OF_LABEL_SECONDS = "start"
LABEL_READER_INTERFACE_END_OF_LABEL_SECONDS = "end"
LABEL_READER_INTERFACE_LOW_FREQUENCY_OF_LABEL_SECONDS = "low"
LABEL_READER_INTERFACE_HIGH_FREQUENCY_OF_LABEL_SECONDS = "high"
LABEL_READER_INTERFACE_VALUE = "value"


class LabelReaderInterface:
    @abc.abstractmethod
    def get_labels_seconds(self) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def get_labels_samples(self) -> list:
        raise NotImplementedError
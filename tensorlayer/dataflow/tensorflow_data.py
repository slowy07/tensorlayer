#! /usr/bin/python
# -*- coding: utf-8 -*-

import tensorflow as tf
import tensorlayer as tl
import numpy as np
__all__ = [
    'Batch',
    'Concat',
    'FromGenerator',
    'FromSlices',
    'Map',
    'Repeat',
    'Shuffle',
    'Zip',
    'Dataloader',
    'Dataset',
    'IterableDataset',
]


class Dataset(object):
    """An abstract class to encapsulate methods and behaviors of datasets.
    All datasets in map-style(dataset samples can be get by a given key) should be a subclass of 'tensorlayer.dataflow.Dataset'.
    ALl subclasses should implement following methods:
    :code:`__getitem__`: get sample from dataset with a given index.
    :code:`__len__`: return dataset sample number.

    Examples
    ----------
    With TensorLayer

    >>> from tensorlayer.dataflow import Dataset
    >>> class mnistdataset(Dataset):
    >>>     def __init__(self, data, label,transform):
    >>>         self.data = data
    >>>         self.label = label
    >>>         self.transform = transform
    >>>     def __getitem__(self, index):
    >>>         data = self.data[index].astype('float32')
    >>>         data = self.transform(data)
    >>>         label = self.label[index].astype('int64')
    >>>         return data, label
    >>>     def __len__(self):
    >>>         return len(self.data)
    >>> train_dataset = mnistdataset(data = X_train, label = y_train ,transform = transform)

    """

    def __init__(self):
        pass

    def __call__(self):

        return self

    def __getitem__(self, idx):
        raise NotImplementedError("'{}' not implement in class "\
                "{}".format('__getitem__', self.__class__.__name__))

    def __len__(self):
        raise NotImplementedError("'{}' not implement in class "\
                "{}".format('__len__', self.__class__.__name__))


class IterableDataset(object):
    """An abstract class to encapsulate methods and behaviors of iterable datasets.
    All datasets in iterable-style (can only get sample one by one sequentially, likea Python iterator) should be a subclass of `tensorlayer.dataflow.IterableDataset`.
    All subclasses should implement following methods:
    :code:`__iter__`: yield sample sequentially.

    Examples
    ----------
    With TensorLayer

    >>> class mnistdataset(IterableDataset):
    >>>     def __init__(self, data, label,transform):
    >>>         self.data = data
    >>>         self.label = label
    >>>         self.transform = transform
    >>>     def __iter__(self):
    >>>         for i in range(len(self.data)):
    >>>             data = self.data[i].astype('float32')
    >>>             data = self.transform(data)
    >>>             label = self.label[i].astype('int64')
    >>>             yield data, label
    >>> train_dataset = mnistdataset(data = X_train, label = y_train ,transform = transform)

    """

    def __init__(self):
        pass

    def __call__(self):

        return self

    def __iter__(self):
        raise NotImplementedError("'{}' not implement in class "\
                "{}".format('__iter__', self.__class__.__name__))


def FromGenerator(generator, output_types, column_names=None):
    """Creates a `Dataset` whose elements are generated by `generator`.

    Parameters
    ----------
    generator: Callable or Iterable
        A generator callable object or an iterable Python object.
    output_types: list or tuple
        Set output data type. This parameter not support in MindSpore backend and Paddle backend.
    column_names: list or tuple
        column names of the dataset. This parameter not support in TensorFlow backend and Paddle backend.

    Returns
    -------
    Dataset
        A Dataset.

    Examples
    ----------
    With TensorLayer

    >>> train_dataset = mnistdataset(data = X_train, label = y_train ,transform = transform)
    >>> train_dataset = tl.dataflow.FromGenerator(train_dataset, output_types=[tl.float32, tl.int64], column_names=['data', 'label'])

    """
    output_types = tuple(output_types)
    return tf.data.Dataset.from_generator(generator, output_types=output_types)


def Batch(dataset, batch_size, drop_last=False):
    """Combine batch_size number of consecutive rows into batches.This function not implement in Paddle backend.

    Parameters
    ----------
    dataset:
        A dataset.
    batch_size: int
        Sample number in a mini-batch.
    drop_last: boolean
        whether drop the last incomplete batch dataset size is not divisible by the batch size.

    Returns
    -------
    Dataset
        A batchDataset.
    """

    return dataset.batch(batch_size=batch_size, drop_remainder=drop_last)


def Concat(datasets):
    """Concatenate the datasets in the input list of datasets.

    Parameters
    ----------
    datasets: dataset
        A list of datasets.

    Returns
    -------
    Dataset
        datasets concatenated.

    Examples
    ----------
    With TensorLayer

    >>> dataset = tl.dataflow.Concat([dataset1, dataset2])

    """

    dataset_num = len(datasets)
    dataset = datasets[0]
    for i in range(1, dataset_num):
        dataset.concatenate(datasets[i])
    return dataset


def FromSlices(datas, column_names=None):
    """Creates a dataset with given data slices.

    Parameters
    ----------
    datas: list or tuple
        Each data should be in shape of [N, …], while N is the sample number.
        Input data will be sliced along the first dimension and generate additional rows
    column_names: list
        List of column names of the dataset. This parameter not support in TensorFlow backend and Paddle backend.

    Returns
    -------
    Dataset
        A dataset.

    Examples
    ----------
    With TensorLayer

    >>> dataset = tl.dataflow.FromSlices([data1, data2])

    """

    return tf.data.Dataset.from_tensor_slices(datas)


def Map(dataset, map_func, input_columns=None):
    """ Maps map_func across the elements of this dataset. This function not implement in Paddle backend.

    Parameters
    ----------
    dataset : Dataset
        A dataset to map.
    map_func : function
        A function mapping a dataset element to another dataset element.
    input_columns: list
        List of column names of the dataset to map. This parameter not support in TensorFlow backend.

    Returns
    -------
    Dataset
        A mapped dataset.

    Examples
    ----------
    With TensorLayer

    >>> dataset = tl.dataflow.Map(dataset, map_func)

    """
    return dataset.map(map_func)


def Repeat(dataset, count=None):
    """ Repeat this dataset count times.  This function not implement in Paddle backend.

    Parameters
    ----------
    dataset : Dataset
        A dataset to repeat.
    count : int
        The number of times the dataset should be repeated. The default behavior (if count is None or -1) is for the dataset be repeated indefinitely.

    Returns
    -------
    Dataset
        A repeated dataset.

    Examples
    ----------
    With TensorLayer

    >>> dataset = tl.dataflow.Repeat(dataset, 2)

    """
    return dataset.repeat(count=count)


def Shuffle(dataset, buffer_size):
    """ Randomly shuffles the elements of this dataset.This function not implement in Paddle backend.

    Parameters
    ----------
    dataset : Dataset
        A dataset to shuffle.
    buffer_size : int
        The number of elements from this dataset from which the new dataset will sample.

    Returns
    -------
    Dataset
        A shuffled dataset.

    Examples
    ----------
    With TensorLayer

    >>> dataset = tl.dataflow.Shuffle(dataset, 2000)

    """
    return dataset.shuffle(buffer_size, seed=None, reshuffle_each_iteration=True)


def Zip(datasets):
    """ Creates a Dataset by zipping together the given datasets.This function not implement in Paddle backend.

    Parameters
    ----------
    datasets : list
        A list of datasets to zip.

    Returns
    -------
    Dataset
        A zip dataset.

    Examples
    ----------
    With TensorLayer

    >>> dataset = tl.dataflow.Zip([dataset1, dataset2])

    """
    return tf.data.Dataset.zip(datasets)


def Dataloader(dataset, batch_size, shuffle=False, drop_last=False, shuffle_buffer_size=10000):
    """ Creates a Datasetloader to trian network. We recommend using this function.

    Parameters
    ----------
    dataset : Dataset
        the dataset to load data from.
    batch_size: int or None
        sample number in a mini-batch.
    shuffle: boolean
        whther to shuffle indices order before genrate batch indices.
    drop_last: boolean
        whether drop the last incomplete batch dataset size is not divisible by the batch size.
    shuffle_buffer_size: int
        The number of elements from this dataset from which the new dataset will sample. This parameter not support in Paddle backend.

    Returns
    -------
    DataLoader
        an iterable object for data iterating, each elemnet of the generated data is a Tensor.

    Examples
    ----------
    With TensorLayer

    >>> from tensorlayer.dataflow import Dataset
    >>> class mnistdataset(Dataset):
    >>>     def __init__(self, data, label,transform):
    >>>         self.data = data
    >>>         self.label = label
    >>>         self.transform = transform
    >>>     def __getitem__(self, index):
    >>>         data = self.data[index].astype('float32')
    >>>         data = self.transform(data)
    >>>         label = self.label[index].astype('int64')
    >>>         return data, label
    >>>     def __len__(self):
    >>>         return len(self.data)
    >>> train_dataset = mnistdataset(data = X_train, label = y_train ,transform = transform)
    >>> train_dataset = tl.dataflow.FromGenerator(train_dataset, output_types=[tl.float32, tl.int64], column_names=['data', 'label'])
    >>> train_dataloader = tl.dataflow.Dataloader(train_dataset, batch_size=128, shuffle=True, drop_last=False, shuffle_buffer_size=2000)

    """

    if shuffle:
        dataset = Shuffle(dataset, buffer_size=shuffle_buffer_size)

    dataset = Batch(dataset, batch_size=batch_size, drop_last=drop_last)
    dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

    return dataset
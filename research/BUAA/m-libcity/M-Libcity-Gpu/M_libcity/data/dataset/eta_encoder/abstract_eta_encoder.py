from logging import getLogger


class AbstractETAEncoder(object):
    """ETA Encoder

    ETA Encoder is used to encode the spatiotemporal information in trajectory.
    We abstract the encoding operation from the Dataset Module to facilitate developers
    to achive more flexible and diverse trajectory representation extraction. It is worth
    noting that the representation extraction involved here is not learnable and fixed.
    Any learnable representation extraction, e.g. embedding, should be emplemented in
    Model Module.

    Attributes:
        config (libcity.ConfigParser): The configuration of the encoder.
        pad_item (dict): The key is a feature's name and the value should be corresponding
            padding value. If a feature dose not need to be padded, don't insert it into
            this dict. In other word, libcity.dataset.Batch will pad all features in pad_item.keys().
        feature_dict (dict): The key is a feature's name and the value should be the data type of
            the corresponding feature. When libcity.dataset.Batch converts the encoded trajectory tuple
            to tensor, It will refer to this attribute to know the feature name and data type corresponding
            to each element in the tuple.
        data_feature (dict): The data_feature contains the statistics features of the encoded dataset, which is
            used to init the model. For example, if the model use nn.Embedding to embed location id and time id,
            the data_feature should contain loc_size and time_size to tell model how to init the embedding layer.
    """

    def __init__(self, config):
        """Init Encoder with its config

        Args:
            config (libcity.ConfigParser): Dict-like Object. Can access any config by config[key].
        """
        self.config = config
        self._logger = getLogger()
        self.pad_item = {}
        self.feature_dict = {}
        self.data_feature = {}
        self.cache_file_name = ''

    def encode(self, uid, trajectories, dyna_feature_column):
        """Encode trajectories of user uid.

        Args:
            uid (int): The uid of user. If there is no need to encode uid, just keep it.
            trajectories (list of trajectory): The trajectories of user. Each trajectory is
            a sequence of spatiotemporal point. The spatiotemporal point is represented by
            a list. Thus, a trajectory is represented by a list of lists. For example:
                trajectory1 = [
                    [dyna_id, type, time, entity_id, traj_id, coordinates/location, properties],
                    [dyna_id, type, time, entity_id, traj_id, coordinates/location, properties],
                    .....
                ]
            Every spatiotemporal tuple contains all useful information in a record of the Raw
            Data (refer to corresponding .dyna file for details). In addition, the trajectories
            are represented as:
                [
                    [ # trajectory1
                        [dyna_id, type, time, entity_id, traj_id, coordinates/location, properties],
                        [dyna_id, type, time, entity_id, traj_id, coordinates/location, properties],
                        ...
                    ],
                    trajectory2,
                    ...
                ]
            dyna_feature_column (dict): The key is a feature's name and the value should be corresponding
                column id in .dyna file.

        Returns:
            list: The return value of this function is the list of encoded trajectories.
            Same as the input format, each encoded trajectory should be a tuple, which contains
            all features extracted from the input trajectory. The encoded trajectory will
            subsequently be converted to a tensor and then directly input to the model.
            (see more in libcity.Batch)
            Take the DeeptteEncoder as an example.
                encoded_trajectory = [current_longi, current_lati, current_tim, current_dis, current_state,
                                      uid, weekid, timeid, dist, time]
            Please make sure the order of the features in the list is consistent with the order
            of the features in self.feature_dict.
        """

    def gen_data_feature(self):
        """After encode all trajectories, this method will be called to tell encoder that you can generate the
        data_feature and pad_item
        """

from abc import ABCMeta, abstractmethod


class ISpeke:
    __metaclass__ = ABCMeta

    @abstractmethod
    def initialize(self, user_number, m_id):
        pass

    @abstractmethod
    def set_password(self, user_number, m_id, password):
        pass

    @abstractmethod
    def initialize_user_instance(self, user_instance):
        pass

    @abstractmethod
    def terminate_user_instance(self, user_instance):
        pass

    @abstractmethod
    def test_instance_password(self, user_instance, password_guess):
        pass

    @abstractmethod
    def get_key(self, user_instance):
        pass

    @abstractmethod
    def send_key(self, user_instance, key):
        pass

    @abstractmethod
    def get_challenge(self, user_instance):
        pass

    @abstractmethod
    def send_challenge(self, user_instance, challenge):
        pass

    @abstractmethod
    def application(self):
        pass

import abc

class ISpeke():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def initialize_user(self, user_number, m_id):
        pass

    @abc.abstractmethod
    def set_password(self, user_number, m_id, password):
        pass

    @abc.abstractmethod
    def initialize_user_instance(self, user_instance, m_id, role, pid):
        pass

    @abc.abstractmethod
    def terminate_user_instance(self, user_instance):
        pass

    @abc.abstractmethod
    def test_instance_password(self, user_instance, password_guess):
        pass

    @abc.abstractmethod
    def get_key(self, user_instance):
        pass

    @abc.abstractmethod
    def send_key(self, user_instance, key):
        pass

    @abc.abstractmethod
    def get_challenge(self, user_instance):
        pass

    @abc.abstractmethod
    def send_challenge(self, user_instance, challenge):
        pass

    @abc.abstractmethod
    def application(self):
        pass


import mock

from base_test import BaseTestCase
from app.email_sender import send_mail


class TestEmailSender(BaseTestCase):

    @mock.patch('app.email_sender.flask_mail')
    def test_send_mail(self, mock_mail):
        mock_data = mock.MagicMock()
        mock_app = mock.MagicMock()
        mock_app.user.email = 'user'
        send_mail(mock_app, mock_data, 'application/json', sender='a@a.a')
        mock_mail.Mail.assert_called_once_with(mock_app)
        mock_mail.Message.assert_called_once_with('Report',
                                                  recipients=['user'],
                                                  sender='a@a.a')
        mock_mail.Mail.return_value.send.\
            assert_called_once_with(mock_mail.Message.return_value)

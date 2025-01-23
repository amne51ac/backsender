import argparse
from unittest.mock import MagicMock, patch

from app.backsender import (
    generate_random_emails,
    main,
    send_spoofed_emails,
    start_smtp_server,
)


def test_generate_random_emails():
    """
    Test the generation of random email addresses.
    """
    domain = "example.com"
    num_emails = 5
    emails = generate_random_emails(domain, num_emails)

    # Check if the correct number of emails is generated
    assert len(emails) == num_emails

    # Verify the domain of generated emails
    for email in emails:
        assert email.endswith(f"@{domain}")


@patch("smtplib.SMTP", autospec=True)
def test_send_spoofed_emails(mock_smtp):
    """
    Test sending spoofed emails using a mocked SMTP server.
    """
    smtp_server = "smtp.testserver.com"
    smtp_port = 587
    smtp_user = "user"
    smtp_password = "password"
    spoofed_senders = ["spoof1@example.com"]
    domain_list = ["target.com"]
    num_emails_per_domain = 2

    # Set up a mock SMTP server connection
    mock_conn = MagicMock()
    mock_smtp.return_value = mock_conn

    # Call the function to test
    send_spoofed_emails(
        smtp_server,
        smtp_port,
        smtp_user,
        smtp_password,
        spoofed_senders,
        domain_list,
        num_emails_per_domain,
    )

    # Verify correct SMTP server connection and authentication
    mock_smtp.assert_called_once_with(smtp_server, smtp_port)

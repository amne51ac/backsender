import argparse
import asyncio
import logging
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Message

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class CustomSMTPHandler(Message):
    """
    Custom handler to process incoming SMTP messages for debugging purposes.
    Prints out message details instead of sending them.
    """

    async def handle_DATA(self, server, session, envelope) -> str:
        """
        Handle incoming SMTP DATA command.

        Args:
            server: The SMTP server instance.
            session: The SMTP session instance.
            envelope: The SMTP envelope containing the message.

        Returns:
            str: SMTP response code.
        """
        logger.info("Message from: %s", envelope.mail_from)
        logger.info("Message to: %s", envelope.rcpt_tos)
        logger.debug(
            "Message data: %s", envelope.content.decode("utf8", errors="replace")
        )
        return "250 Message accepted for delivery"


def start_smtp_server(host: str = "127.0.0.1", port: int = 1025) -> None:
    """
    Start an asynchronous SMTP server using aiosmtpd.

    Args:
        host (str): Host address for the server. Default is '127.0.0.1'.
        port (int): Port number for the server. Default is 1025.
    """
    handler = CustomSMTPHandler()
    controller = Controller(handler, hostname=host, port=port)
    controller.start()
    logger.info("SMTP server running on %s:%d", host, port)


def generate_random_emails(domain: str, num: int) -> List[str]:
    """
    Generate a list of random non-existent email addresses for a given domain.

    Args:
        domain (str): The domain name to append to generated emails.
        num (int): The number of random email addresses to generate.

    Returns:
        List[str]: A list of generated email addresses.
    """
    emails = [
        f"{''.join(random.choices(string.ascii_lowercase, k=8))}@{domain}"
        for _ in range(num)
    ]
    logger.debug("Generated emails: %s", emails)
    return emails


def send_spoofed_emails(
    smtp_server: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    spoofed_senders: List[str],
    domain_list: List[str],
    num_emails_per_domain: int,
) -> None:
    """
    Send spoofed emails to randomly generated addresses for each domain.

    Args:
        smtp_server (str): The SMTP server to connect to.
        smtp_port (int): The port number for the SMTP server.
        smtp_user (str): The username for SMTP authentication.
        smtp_password (str): The password for SMTP authentication.
        spoofed_senders (List[str]): List of email addresses to use as spoofed senders.
        domain_list (List[str]): Target domains for generating recipient addresses.
        num_emails_per_domain (int): Number of random emails to send per domain.
    """
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            logger.info("Connecting to SMTP server %s:%d", smtp_server, smtp_port)
            server.starttls()
            logger.debug("Starting TLS")
            server.login(smtp_user, smtp_password)
            logger.info("Logged in as %s", smtp_user)

            for domain in domain_list:
                recipient_list = generate_random_emails(domain, num_emails_per_domain)
                for spoofed_sender in spoofed_senders:
                    message = MIMEMultipart()
                    message["From"] = spoofed_sender
                    message["Subject"] = "Test Email"
                    body = "This is a test email to a non-existent address."
                    message.attach(MIMEText(body, "plain"))

                    for recipient in recipient_list:
                        try:
                            server.sendmail(
                                spoofed_sender, recipient, message.as_string()
                            )
                            logger.info(
                                "Email from %s sent to %s", spoofed_sender, recipient
                            )
                        except Exception as e:
                            logger.error(
                                "Failed to send email from %s to %s: %s",
                                spoofed_sender,
                                recipient,
                                e,
                            )
    except Exception as e:
        logger.error("Failed to connect to SMTP server: %s", e)


def main() -> None:
    """
    Main function to parse arguments and execute the appropriate mode.
    """
    parser = argparse.ArgumentParser(
        description="Send spoofed emails or run a simulated SMTP server for testing purposes."
    )
    parser.add_argument(
        "--mode",
        choices=["send", "simulate"],
        required=True,
        help='Mode to operate in: "send" to send emails, "simulate" to run an SMTP server.',
    )
    parser.add_argument("--smtp-server", help="SMTP server address.")
    parser.add_argument(
        "--smtp-port", type=int, default=587, help="SMTP server port. Default is 587."
    )
    parser.add_argument("--smtp-user", help="SMTP user for login.")
    parser.add_argument("--smtp-password", help="SMTP password for login.")
    parser.add_argument(
        "--spoofed-senders",
        nargs="+",
        help="List of email addresses to spoof as the senders.",
    )
    parser.add_argument("--domain-list", nargs="+", help="List of target domains.")
    parser.add_argument(
        "--num-emails-per-domain",
        type=int,
        default=10,
        help="Number of random emails to generate per domain.",
    )
    parser.add_argument(
        "--server-port",
        type=int,
        default=1025,
        help="Port for the simulated SMTP server. Default is 1025.",
    )
    args = parser.parse_args()

    if args.mode == "simulate":
        start_smtp_server(port=args.server_port)
        asyncio.get_event_loop().run_forever()
    elif args.mode == "send":
        if not (
            args.smtp_server
            and args.smtp_user
            and args.smtp_password
            and args.spoofed_senders
            and args.domain_list
        ):
            logger.error("All email sending parameters must be provided in send mode.")
            return

        send_spoofed_emails(
            smtp_server=args.smtp_server,
            smtp_port=args.smtp_port,
            smtp_user=args.smtp_user,
            smtp_password=args.smtp_password,
            spoofed_senders=args.spoofed_senders,
            domain_list=args.domain_list,
            num_emails_per_domain=args.num_emails_per_domain,
        )


if __name__ == "__main__":
    main()

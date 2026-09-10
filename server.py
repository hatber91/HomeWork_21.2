from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs


HOST = "localhost"
PORT = 8000

BASE_DIR = Path(__file__).resolve().parent
HTML_DIR = BASE_DIR / "html"


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP-запросов."""

    def read_html_file(self, filename: str) -> str:
        """Читает HTML-файл и возвращает его содержимое."""

        file_path = HTML_DIR / filename

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def send_html(self, html: str, status_code: int = 200) -> None:
        """Отправляет HTML-ответ клиенту."""

        self.send_response(status_code)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8",
        )

        self.end_headers()

        self.wfile.write(html.encode("utf-8"))

    def do_GET(self) -> None:
        """Обрабатывает GET-запрос."""

        try:
            html = self.read_html_file("contacts.html")

            self.send_html(html)

        except Exception as error:
            print(f"Ошибка при обработке GET-запроса: {error}")

            try:
                html = self.read_html_file("500.html")

            except Exception:
                html = """
                <html>
                    <body>
                        <h1>500</h1>
                        <p>Внутренняя ошибка сервера</p>
                    </body>
                </html>
                """

            self.send_html(
                html,
                status_code=500,
            )

    def do_POST(self) -> None:
        """Обрабатывает POST-запрос."""

        try:
            content_length = int(
                self.headers.get(
                    "Content-Length",
                    0,
                )
            )

            post_data = self.rfile.read(content_length)

            decoded_data = post_data.decode("utf-8")

            form_data = parse_qs(decoded_data)

            print("Получен POST-запрос:")
            print(f"Имя: {form_data.get('name', [''])[0]}")
            print(f"Почта: {form_data.get('email', [''])[0]}")
            print(f"Сообщение: {form_data.get('message', [''])[0]}")

            html = self.read_html_file("contacts.html")

            self.send_html(html)

        except Exception as error:
            print(f"Ошибка при обработке POST-запроса: {error}")

            html = self.read_html_file("500.html")

            self.send_html(
                html,
                status_code=500,
            )


def run_server() -> None:
    """Запускает HTTP-сервер."""

    server = HTTPServer(
        (HOST, PORT),
        SimpleHTTPRequestHandler,
    )

    print(
        f"Сервер запущен: http://{HOST}:{PORT}"
    )

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nСервер остановлен.")

    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
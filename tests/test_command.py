import unittest

from app.command import Command, Redirect


class TestIsRedirect(unittest.TestCase):
    def validate(self, command, fd, file, output, append):
        redirect = Redirect.parse(command)
        self.assertTrue(redirect)
        self.assertEqual(redirect.fd, fd)
        self.assertEqual(redirect.file, file)
        self.assertEqual(redirect.output, output)
        self.assertEqual(redirect.append, append)

    def validate_input(self, command, fd, file):
        self.validate(command, fd, file, False, False)

    def validate_output(self, command, fd, file):
        self.validate(command, fd, file, True, False)

    def validate_append(self, command, fd, file):
        self.validate(command, fd, file, True, True)

    def test_simple(self):
        self.validate_output(">", 1, "")
        self.validate_append(">>", 1, "")
        self.validate_input("<", 0, "")

        self.assertFalse(Redirect.parse("file>"))

    def test_numbered(self):
        self.validate_output("1>", 1, "")
        self.validate_output("2>", 2, "")
        self.validate_output("255>", 255, "")
        self.validate_append("1>>", 1, "")
        self.validate_input("2<", 2, "")

        self.assertFalse(Redirect.parse("1"))

    def test_file(self):
        self.validate_output(">file", 1, "file")
        self.validate_append(">>../file", 1, "../file")
        self.validate_input("</file", 0, "/file")

        self.validate_output("3>file", 3, "file")

        self.assertFalse(Redirect.parse("file"))


class TestCommand(unittest.TestCase):
    def validate(self, tokens, command, args, redirects):
        cmd = Command.parse(tokens)
        self.assertEqual(cmd.command, command)
        self.assertEqual(cmd.args, args)
        self.assertEqual(cmd.redirects, redirects)

    def test_simple(self):
        self.validate(["echo"], "echo", (), ())
        self.validate(["echo", "hello"], "echo", ("hello",), ())

    def test_redirect(self):
        self.validate(
            ["echo", ">file", "hello"],
            "echo",
            ("hello",),
            (Redirect(1, "file", True, False),),
        )

        self.validate(
            ["echo", ">", "file"], "echo", (), (Redirect(1, "file", True, False),)
        )
        self.validate(
            [">file", "echo"], "echo", (), (Redirect(1, "file", True, False),)
        )

    def test_multiple(self):
        self.validate(
            ["echo", ">file", "hello", "2>>file2"],
            "echo",
            ("hello",),
            (Redirect(1, "file", True, False), Redirect(2, "file2", True, True)),
        )

        self.validate(
            ["echo", ">file", "hello", "1>file2"],
            "echo",
            ("hello",),
            (Redirect(1, "file", True, False), Redirect(1, "file2", True, False)),
        )


if __name__ == "__main__":
    unittest.main()

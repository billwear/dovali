# validators.py

import abc
import hunspell
import subprocess


class Validator(abc.ABC):
    """Abstract validator interface"""

    @abc.abstractmethod
    def validate(self, file_path):
        """Validate the specified file and return issues"""
        pass


class PlaceholderValidator(Validator):
    """Placeholder validator with dummy success/failure"""

    def validate(self, file_path):
        # Dummy validation: Always succeed
        return []


class HunspellValidator(Validator):
    """Validator that runs hunspell for spell checking"""

    def __init__(self):
        # Initialize hunspell
        self.hunspell_obj = hunspell.HunSpell(
            "/usr/share/hunspell/en_US.dic", "/usr/share/hunspell/en_US.aff"
        )

    def validate(self, file_path):
        issues = []
        with open(file_path, "r") as file:
            for line_num, line in enumerate(file, start=1):
                words = line.strip().split()
                for word in words:
                    if not self.hunspell_obj.spell(word):
                        issues.append(f"Spelling error at line {line_num}: {word}")
        return issues


class CommandLineValidator(Validator):
    """Validator that runs a command line on the file"""

    def __init__(self, command):
        self.command = command

    def validate(self, file_path):
        try:
            # Run the command on the file using subprocess
            result = subprocess.run(
                [self.command, file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            if result.returncode != 0:
                # If the command returns a non-zero exit code, it indicates an error
                error_message = result.stderr.strip()
                return [f"Validation failed: {error_message}"]
            else:
                # Return an empty list to indicate no issues found during validation
                return []
        except Exception as e:
            return [f"Validation failed with an error: {str(e)}"]


class ValidatorConfig:
    """Config schema for validators"""

    # Define your validator classes here
    VALIDATORS = {
        "placeholder": PlaceholderValidator,
        "hunspell": HunspellValidator,  # Add the HunspellValidator
        "command_line": CommandLineValidator,  # Add the CommandLineValidator
        # Add more validator classes here as needed
    }

    @classmethod
    def get_validator(cls, name):
        """Get a validator class by name"""
        return cls.VALIDATORS.get(name)

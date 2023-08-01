# validators.py

import abc

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

class ValidatorConfig:
    """Config schema for validators"""

    # Define your validator classes here
    VALIDATORS = {
        "placeholder": PlaceholderValidator,
        # Add more validator classes here as needed
    }

    @classmethod
    def get_validator(cls, name):
        """Get a validator class by name"""
        return cls.VALIDATORS.get(name)

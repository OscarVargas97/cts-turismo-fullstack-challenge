import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run pre-commit hooks for linting and testing"

    def handle(self, *args, **kwargs):
        # Comando pre-commit
        command = "pre-commit run --all-files"

        self.stdout.write(self.style.SUCCESS(f"Running: {command}"))
        result = subprocess.run(command, shell=True)

        if result.returncode != 0:
            self.stderr.write(self.style.ERROR("Pre-commit hooks failed"))
        else:
            self.stdout.write(self.style.SUCCESS("Pre-commit hooks passed"))

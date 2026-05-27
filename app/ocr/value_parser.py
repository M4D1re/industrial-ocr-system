import re


class OCRValueParser:
    """
    Parses numeric values from OCR raw text.
    """

    @staticmethod
    def parse(raw_text: str) -> float | None:
        """
        Parses OCR text to numeric value.

        Supported examples:
        - 123
        - 123.45
        - 123,45
        - -12.5
        - 00:54,71 -> 54.71
        - 01:14.74 -> 74.74
        """

        if not raw_text:
            return None

        text = raw_text.strip()

        text = text.replace(" ", "")
        text = text.replace(",", ".")

        time_value = OCRValueParser._parse_time_like_value(text)

        if time_value is not None:
            return time_value

        number_value = OCRValueParser._parse_regular_number(text)

        return number_value

    @staticmethod
    def _parse_time_like_value(text: str) -> float | None:
        """
        Parses values like 00:54.71 or 01:14.74.

        Converts them to seconds.
        """

        match = re.search(
            r"(?P<minutes>\d{1,2})[:;](?P<seconds>\d{1,2})(?:[.](?P<fraction>\d+))?",
            text,
        )

        if match is None:
            return None

        minutes = int(match.group("minutes"))
        seconds = int(match.group("seconds"))

        fraction_raw = match.group("fraction") or "0"

        fraction = float(f"0.{fraction_raw}")

        return minutes * 60 + seconds + fraction

    @staticmethod
    def _parse_regular_number(text: str) -> float | None:
        """
        Parses normal numeric values.
        """

        match = re.search(
            r"-?\d+(?:\.\d+)?",
            text,
        )

        if match is None:
            return None

        try:
            return float(match.group(0))
        except ValueError:
            return None
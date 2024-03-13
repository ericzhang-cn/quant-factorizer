import arrow
import click


class ArrowType(click.ParamType):
    """
    Custom Click parameter type for parsing Arrow date and time objects.
    """

    name = 'arrow'

    def convert(self, value, param, ctx):
        """
            Convert the input value to an Arrow date and time object.

        :param value: The input date and time value.
        :type value: str
        :param param: The parameter object.
        :type param: click.Parameter
        :param ctx: The context object.
        :type ctx: click.Context
        :return: The converted Arrow date and time object.
        :rtype: arrow.Arrow
        :raises click.BadParameter: If the input value cannot be parsed as a valid date and time format.
        """
        try:
            return arrow.get(value)
        except arrow.parser.ParserError:
            self.fail(f'Invalid date and time format: {value}', param, ctx)

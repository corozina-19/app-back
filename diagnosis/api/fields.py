from rest_framework.fields import CharField


class MultiTypeResponseField(CharField):
    def to_internal_value(self, data):
        """
        To internal value for Charfield only allow number and strings as posible values, as we work with
        yes/no answer we will accept booleans as a posibility.
        :param data: data to convert to internal value
        :return: data
        """
        value = data

        if isinstance(data, (str, int, float,)):
            value = str(data)

        return value.strip() if self.trim_whitespace and isinstance(value, str) else value

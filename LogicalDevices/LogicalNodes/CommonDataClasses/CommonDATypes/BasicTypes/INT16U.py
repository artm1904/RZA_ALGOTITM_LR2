import struct

class INT16U:
    """
    Класс-обертка над unsigned 16-bit integer (INT16U).
    """

    MIN_VALUE = 0
    MAX_VALUE = 65535  # 2**16 - 1

    def __init__(self, value=0):
        """
        Инициализирует объект UInt16Wrapper.

        Args:
            value (int, optional): Начальное значение uint16. Defaults to 0.

        Raises:
            TypeError: Если value не является целым числом.
            ValueError: Если value выходит за пределы диапазона uint24 (0 to 2^16- 1).
        """
        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")

        if not (self.MIN_VALUE <= value <= self.MAX_VALUE):
            raise ValueError(
                f"Value must be within the range of uint24 ({self.MIN_VALUE} to {self.MAX_VALUE})."
            )

        self._value = value

    @property
    def value(self):
        """
        Возвращает текущее значение uint16.
        """
        return self._value

    @value.setter
    def value(self, new_value):
        """
        Устанавливает новое значение uint16.

        Args:
            new_value (int): Новое значение uint16.

        Raises:
            TypeError: Если new_value не является целым числом.
            ValueError: Если new_value выходит за пределы диапазона uint24 (0 to 2^16 - 1).
        """
        if not isinstance(new_value, int):
            raise TypeError("Value must be an integer.")

        if not (self.MIN_VALUE <= new_value <= self.MAX_VALUE):
            raise ValueError(
                f"Value must be within the range of uint16 ({self.MIN_VALUE} to {self.MAX_VALUE})."
            )

        self._value = new_value

    def __str__(self):
        """
        Возвращает строковое представление объекта.
        """
        return str(self._value)

    def __repr__(self):
        """
        Возвращает строковое представление объекта для отладки.
        """
        return f"UInt16Wrapper({self._value})"

    def __int__(self):
        """
        Позволяет преобразовывать объект UInt16Wrapper в int с помощью int().
        """
        return self._value

    def __eq__(self, other):
        """
        Переопределяет оператор ==.
        """
        if isinstance(other, INT16U):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        else:
            return False

    def to_bytes(self, byte_order='little'):
        """
        Преобразует значение uint16 в байты.

        Args:
            byte_order (str, optional): Порядок байтов ('little' или 'big'). Defaults to 'little'.

        Returns:
            bytes: Байтовое представление uint16 (2 байта).
        """
        return struct.pack('<I'[:3] if byte_order == 'little' else '>I'[:3], self._value)

    @classmethod
    def from_bytes(cls, byte_data, byte_order='little'):
        """
        Создает объект UInt16Wrapper из байтов.

        Args:
            byte_data (bytes): Байты, представляющие uint16 (2 байта).
            byte_order (str, optional): Порядок байтов ('little' или 'big'). Defaults to 'little'.

        Returns:
            UInt16Wrapper: Объект UInt16Wrapper, созданный из байтов.

        Raises:
            ValueError: Если длина byte_data не равна 2.
        """
        if len(byte_data) != 2:
            raise ValueError("Byte data must be 2 bytes long for uint16.")

        return cls(struct.unpack('<I' if byte_order == 'little' else '>I', byte_data + b'\0')[0])



# # Пример использования
# if __name__ == "__main__":
#     num1 = UInt24Wrapper(1234567)
#     print(f"num1: {num1}")
#
#     print(f"num1 == 1234567: {num1 == 1234567}")
#
#     # Преобразование в байты и обратно
#     byte_data = num1.to_bytes(byte_order='big')
#     print(f"Bytes (big-endian): {byte_data}")
#     num2 = UInt24Wrapper.from_bytes(byte_data, byte_order='big')
#     print(f"From bytes (big-endian): {num2}")
#
#     byte_data = num1.to_bytes(byte_order='little')
#     print(f"Bytes (little-endian): {byte_data}")
#     num2 = UInt24Wrapper.from_bytes(byte_data, byte_order='little')
#     print(f"From bytes (little-endian): {num2}")
#
#     try:
#         num3 = UInt24Wrapper(2**24)  # Вызовет ValueError
#     except ValueError as e:
#         print(f"Error: {e}")  # Error: Value must be within the range of uint24 (0 to 16777215).
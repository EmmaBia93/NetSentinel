def cantidad_horas_activo(tiempo: int) -> str:
        """
        Converts seconds into a string of format dd:hh:mm.

        Args:
            tiempo (int): The time in seconds.

        Returns:
            str: The formatted time string.
        """
        dias = tiempo // (24 * 60 * 60)
        tiempo %= (24 * 60 * 60)
        horas = tiempo // (60 * 60)
        tiempo %= (60 * 60)
        minutos = tiempo // 60
        return f"{dias}dias:{horas}hs:{minutos}min"
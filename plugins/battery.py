from .worker import Worker


class PluginBattery(Worker):
    """Display current battery/AC status

    """
    def __init__(self, **kwargs):
        Worker.__init__(self, **kwargs)

    def _icon_select(self, capacity):
        """Given capacity, return the appropriate battery icon

        """
        if capacity > 75:
            icon = self.cfg.battery.batt_icon_full
        elif capacity > 50 and capacity <= 75:
            icon = self.cfg.battery.batt_icon_34
        elif capacity > 25 and capacity <= 50:
            icon = self.cfg.battery.batt_icon_12
        elif capacity > int(self.cfg.battery.low) and capacity <= 25:
            icon = self.cfg.battery.batt_icon_14
        else:
            icon = self.cfg.battery.batt_icon_empty
        return icon

    def _update_data(self):
        with open(self.cfg.battery.batt_status) as f:
            status = f.readline().strip()
        with open(self.cfg.battery.batt_charge) as f:
            capacity = int(f.readline().strip())
            icon = self._icon_select(capacity)
        if status == "Discharging" and capacity > int(self.cfg.battery.warn):
            capacity_str = "{} {}".format(icon, str(capacity))
            out = self._color_text(capacity_str, fg=self.cfg.battery.color_fg)
        elif status == "Discharging" and capacity > int(self.cfg.battery.low):
            capacity_str = "{} {}".format(icon, str(capacity))
            out = self._color_text(capacity_str, fg=self.cfg.battery.color_bg,
                                   bg=self.cfg.battery.color_fg)
        elif status == "Discharging" and capacity <= int(self.cfg.battery.low):
            capacity_str = "{} {}".format(icon, str(capacity))
            out = self._err_text(capacity_str)
        elif status == "Charging":
            capacity_str = "{} {}".format(self.cfg.battery.ac_icon,
                                          str(capacity))
            out = self._color_text(capacity_str, fg=self.cfg.battery.color_fg,
                                   bg=self.cfg.battery.color_bg)
        else:
            out = ""
        return (self.__module__, self._out_format(out))

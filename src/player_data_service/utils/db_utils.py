from datetime import datetime


def build_update_fields(updated_dto) -> str:
    modify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    values_dict = {}

    for k, v in dict(updated_dto).items():
        if v is not None:
            values_dict[k] = v

    update_fields = [f"{k}='{v}'" for k, v in dict(values_dict).items()]
    update_fields.append(f"modified='{modify_time}'")
    return ", ".join(update_fields)

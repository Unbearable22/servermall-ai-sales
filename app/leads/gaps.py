QUESTIONS = [
    ("purpose", "Для каких задач нужен сервер: виртуализация, 1С, базы данных, хранение или другое?"),
    ("server_quantity", "Сколько серверов планируется приобрести?"),
    ("cpu_count", "Сколько физических процессоров требуется в одном сервере?"),
    ("cpu_cores", "Сколько физических ядер нужно?"),
    ("cpu_frequency_ghz", "Есть ли требования к базовой частоте CPU в ГГц?"),
    ("ram_gb", "Какой общий объём оперативной памяти требуется?"),
    ("ram_expand_gb", "Планируется ли расширение памяти?"),
    ("drive_type", "Какие накопители нужны: SATA, SAS или NVMe?"),
    ("drive_count", "Сколько накопителей требуется?"),
    ("drive_capacity_tb", "Какой объём каждого накопителя?"),
    ("raid_level", "Нужен ли определённый уровень RAID?"),
    ("network_speed_gbps", "Какая скорость сетевых портов требуется?"),
    ("network_port_count", "Сколько сетевых портов нужно?"),
    ("psu_redundancy", "Нужны ли резервные блоки питания?"),
    ("idrac_license", "Нужна ли лицензия iDRAC Enterprise?"),
    ("warranty_years", "На какой срок требуется гарантия?"),
    ("budget_rub", "Есть ли ориентир по бюджету?"),
    ("delivery_city", "В какой город нужна доставка?"),
    ("purchase_deadline", "К какому сроку планируете закупку?"),
]
STATUSES = {"CONFIRMED", "UNKNOWN", "NOT_SPECIFIED", "NOT_APPLICABLE"}

def next_questions(requirements: dict, limit: int = 2) -> list[dict]:
    result = []
    for field, question in QUESTIONS:
        record = requirements.get(field)
        if not record or record.get("status") == "NOT_SPECIFIED":
            result.append({"field": field, "question": question})
        if len(result) >= limit:
            break
    return result

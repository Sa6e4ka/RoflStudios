from loguru import logger

# Логгеры для дебага и эррора, файлы отправляются по команде /loggs
INFO = logger.add("backend/Loggs/loggs.log", format="--------\n{time:DD-MM HH}\n{level}\n{message}\n--------", level='INFO', rotation='1 week')


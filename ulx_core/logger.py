#!/usr/bin/env python3
"""
ULX Logger - Sistema de logging estruturado
"""

import sys
import time
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
import json


class LogLevel(Enum):
    """Níveis de log"""
    DEBUG = auto()
    INFO = auto()
    SUCCESS = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()
    
    def __str__(self):
        return self.name


class LogOutput(Enum):
    """Destinos de saída para logs"""
    CONSOLE = auto()
    FILE = auto()
    BOTH = auto()
    NONE = auto()


@dataclass
class LogEntry:
    """Entrada de log individual"""
    level: LogLevel
    message: str
    timestamp: float = field(default_factory=time.time)
    source: Optional[str] = None
    line: Optional[int] = None
    context: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'level': self.level.name,
            'message': self.message,
            'timestamp': self.timestamp,
            'datetime': datetime.fromtimestamp(self.timestamp).isoformat(),
            'source': self.source,
            'line': self.line,
            'context': self.context or {}
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    def __str__(self):
        dt = datetime.fromtimestamp(self.timestamp).strftime("%H:%M:%S.%f")[:-3]
        source_str = f"[{self.source}]" if self.source else ""
        return f"[{dt}] {self.level.name:8} {source_str} {self.message}"


class ULXLogger:
    """Logger estruturado para ULX"""
    
    LEVEL_COLORS = {
        LogLevel.DEBUG: '\033[90m',      # Gray
        LogLevel.INFO: '\033[94m',       # Blue
        LogLevel.SUCCESS: '\033[92m',    # Green
        LogLevel.WARNING: '\033[93m',    # Yellow
        LogLevel.ERROR: '\033[91m',      # Red
        LogLevel.CRITICAL: '\033[95m',   # Magenta
    }
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    LEVEL_PRIORITY = {
        LogLevel.DEBUG: 0,
        LogLevel.INFO: 1,
        LogLevel.SUCCESS: 2,
        LogLevel.WARNING: 3,
        LogLevel.ERROR: 4,
        LogLevel.CRITICAL: 5,
    }
    
    def __init__(self, name: str = "ULX", level: LogLevel = LogLevel.INFO,
                 output: LogOutput = LogOutput.CONSOLE, 
                 log_file: Optional[str] = None,
                 use_colors: bool = True,
                 verbose: bool = False):
        self.name = name
        self.level = level
        self.output = output
        self.log_file = log_file
        self.use_colors = use_colors and sys.stdout.isatty()
        self.verbose = verbose
        self.entries: List[LogEntry] = []
        self._file_handle = None
        self._stats = {level: 0 for level in LogLevel}
        self._start_time = time.time()
        
        if self.log_file and self.output in (LogOutput.FILE, LogOutput.BOTH):
            self._file_handle = open(self.log_file, 'a', encoding='utf-8')
    
    def _should_log(self, level: LogLevel) -> bool:
        return self.LEVEL_PRIORITY[level] >= self.LEVEL_PRIORITY[self.level]
    
    def _write(self, entry: LogEntry):
        """Escreve entrada de log"""
        self.entries.append(entry)
        self._stats[entry.level] += 1
        
        if self.output in (LogOutput.CONSOLE, LogOutput.BOTH):
            self._write_console(entry)
        
        if self.output in (LogOutput.FILE, LogOutput.BOTH) and self._file_handle:
            self._file_handle.write(str(entry) + '\n')
            self._file_handle.flush()
    
    def _write_console(self, entry: LogEntry):
        """Escreve no console com cores"""
        color = self.LEVEL_COLORS.get(entry.level, '') if self.use_colors else ''
        reset = self.RESET if self.use_colors else ''
        bold = self.BOLD if self.use_colors else ''
        
        prefix = f"{bold}[{self.name}]{reset}"
        level_str = f"{color}[{entry.level.name}]{reset}"
        
        print(f"{prefix} {level_str} {entry.message}")
    
    def debug(self, message: str, source: Optional[str] = None, 
              line: Optional[int] = None, **context):
        """Log de debug"""
        if self._should_log(LogLevel.DEBUG):
            self._write(LogEntry(LogLevel.DEBUG, message, source=source, 
                                line=line, context=context or None))
    
    def info(self, message: str, source: Optional[str] = None,
             line: Optional[int] = None, **context):
        """Log informativo"""
        if self._should_log(LogLevel.INFO):
            self._write(LogEntry(LogLevel.INFO, message, source=source,
                                line=line, context=context or None))
    
    def success(self, message: str, source: Optional[str] = None,
                line: Optional[int] = None, **context):
        """Log de sucesso"""
        if self._should_log(LogLevel.SUCCESS):
            self._write(LogEntry(LogLevel.SUCCESS, message, source=source,
                                line=line, context=context or None))
    
    def warning(self, message: str, source: Optional[str] = None,
                line: Optional[int] = None, **context):
        """Log de aviso"""
        if self._should_log(LogLevel.WARNING):
            self._write(LogEntry(LogLevel.WARNING, message, source=source,
                                line=line, context=context or None))
    
    def error(self, message: str, source: Optional[str] = None,
              line: Optional[int] = None, **context):
        """Log de erro"""
        if self._should_log(LogLevel.ERROR):
            self._write(LogEntry(LogLevel.ERROR, message, source=source,
                                line=line, context=context or None))
    
    def critical(self, message: str, source: Optional[str] = None,
                 line: Optional[int] = None, **context):
        """Log crítico"""
        if self._should_log(LogLevel.CRITICAL):
            self._write(LogEntry(LogLevel.CRITICAL, message, source=source,
                                line=line, context=context or None))
    
    def compile_step(self, step: int, total: int, description: str):
        """Log de etapa de compilação"""
        self.info(f"[{step}/{total}] {description}", source="Compilador")
    
    def compile_progress(self, current: int, total: int, description: str = ""):
        """Barra de progresso da compilação"""
        percent = (current / total) * 100 if total > 0 else 0
        bar_length = 30
        filled = int(bar_length * current / total) if total > 0 else 0
        bar = '█' * filled + '░' * (bar_length - filled)
        
        msg = f"[{bar}] {percent:.1f}%"
        if description:
            msg += f" - {description}"
        
        if self.verbose:
            self.info(msg, source="Progresso")
    
    def timing(self, operation: str, elapsed: float):
        """Log de tempo de operação"""
        unit = "ms" if elapsed < 1 else "s"
        value = elapsed * 1000 if elapsed < 1 else elapsed
        self.debug(f"{operation}: {value:.2f}{unit}", source="Timing")
    
    def get_stats(self) -> Dict[str, int]:
        """Retorna estatísticas de log"""
        return {level.name: count for level, count in self._stats.items()}
    
    def get_elapsed_time(self) -> float:
        """Retorna tempo decorrido desde a criação"""
        return time.time() - self._start_time
    
    def export_json(self, filename: str):
        """Exporta logs para JSON"""
        data = {
            'logger_name': self.name,
            'start_time': self._start_time,
            'elapsed': self.get_elapsed_time(),
            'stats': self.get_stats(),
            'entries': [entry.to_dict() for entry in self.entries]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def print_summary(self):
        """Imprime resumo de logs"""
        elapsed = self.get_elapsed_time()
        print(f"\n{'='*50}")
        print(f"  RESUMO DO LOG - {self.name}")
        print(f"{'='*50}")
        print(f"  Tempo: {elapsed:.2f}s")
        for level, count in self._stats.items():
            if count > 0:
                icon = "✅" if level in (LogLevel.INFO, LogLevel.SUCCESS) else "⚠️" if level == LogLevel.WARNING else "❌"
                print(f"  {icon} {level.name}: {count}")
        print(f"{'='*50}\n")
    
    def clear(self):
        """Limpa entradas de log"""
        self.entries.clear()
        self._stats = {level: 0 for level in LogLevel}
    
    def close(self):
        """Fecha o logger"""
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if self.verbose:
            self.print_summary()
    
    def __del__(self):
        self.close()

from flask import Flask, jsonify, request
from flask_cors import CORS
import psutil
import GPUtil
import io
import base64
import pygetwindow as gw
import mss
import mss.tools
from typing import Dict, List, Any
from dataclasses import dataclass
import win32gui
import win32con

# Configuration
class Config:
    """Application configuration settings."""
    PORT = 3000
    DEBUG = False
    SCREENSHOT_QUALITY = 100
    API_PREFIX = ''

# Data Models
@dataclass
class SystemMetrics:
    """Data class for system metrics."""
    cpu_usage: float
    gpu_info: List[Dict[str, Any]]
    ram_info: Dict[str, Any]

class SystemMonitor:
    """Class responsible for system monitoring operations."""
    
    @staticmethod
    def get_cpu_info() -> Dict[str, float]:
        """Get CPU usage information."""
        return {
            'usage_percent': round(psutil.cpu_percent(interval=1), 2)
        }

    @staticmethod
    def get_gpu_info() -> List[Dict[str, Any]]:
        """Get GPU information for all available GPUs."""
        gpu_info = []
        for gpu in GPUtil.getGPUs():
            gpu_info.append({
                'name': gpu.name,
                'load': round(gpu.load * 100, 2),
                'temperature': round(gpu.temperature, 2),
                'memory_used': round(gpu.memoryUsed, 2),
                'memory_total': round(gpu.memoryTotal, 2),
            })
        return gpu_info

    @staticmethod
    def get_ram_info() -> Dict[str, float]:
        """Get RAM usage information."""
        ram = psutil.virtual_memory()
        return {
            'total': round(ram.total / (1024 ** 2), 2),
            'available': round(ram.available / (1024 ** 2), 2),
            'used_percent': round(ram.percent, 2)
        }

class ScreenshotManager:
    """Class responsible for screenshot operations."""
    
    @staticmethod
    def capture_all_screens() -> List[str]:
        """Capture screenshots from all available monitors."""
        screenshots = []
        with mss.mss() as sct:
            for monitor in sct.monitors[1:]:  # Skip first monitor (represents all monitors combined)
                screenshot = sct.grab(monitor)
                output = io.BytesIO(mss.tools.to_png(screenshot.rgb, screenshot.size))
                base64_string = base64.b64encode(output.getvalue()).decode("utf-8")
                screenshots.append(base64_string)
        return screenshots

class ProcessManager:
    """Class responsible for process management operations."""
    
    @staticmethod
    def get_window_list() -> List[Dict[str, Any]]:
        """Get list of all open windows."""
        return [
            {'hwnd': window._hWnd, 'title': window.title}
            for window in gw.getAllWindows()
            if window.title and win32gui.IsWindowVisible(window._hWnd)
        ]

    @staticmethod
    def close_window(hwnd: int) -> None:
        """Close a window by its handle."""
        if not win32gui.IsWindow(hwnd):
            raise ValueError("Invalid window handle")
        
        if not win32gui.IsWindowVisible(hwnd):
            raise ValueError("Window is not visible")

        # Сначала пробуем закрыть окно "вежливо"
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

# API Routes
def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)

    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    # Routes
    @app.route(f'{Config.API_PREFIX}/system_info', methods=['GET'])
    def get_system_info():
        """Get system information including CPU, GPU, and RAM metrics."""
        try:
            monitor = SystemMonitor()
            metrics = SystemMetrics(
                cpu_usage=monitor.get_cpu_info()['usage_percent'],
                gpu_info=monitor.get_gpu_info(),
                ram_info=monitor.get_ram_info()
            )
            return jsonify({
                'cpu': {'usage_percent': metrics.cpu_usage},
                'gpu': metrics.gpu_info,
                'ram': metrics.ram_info
            })
        except Exception as e:
            app.logger.error(f"Error getting system info: {str(e)}")
            return jsonify({'error': 'Failed to get system information'}), 500

    @app.route(f'{Config.API_PREFIX}/screenshot', methods=['GET'])
    def get_screenshot():
        """Get screenshots from all available monitors."""
        try:
            screenshots = ScreenshotManager.capture_all_screens()
            return jsonify({'screenshots': screenshots})
        except Exception as e:
            app.logger.error(f"Error capturing screenshots: {str(e)}")
            return jsonify({'error': 'Failed to capture screenshots'}), 500

    @app.route(f'{Config.API_PREFIX}/processes', methods=['GET'])
    def get_processes():
        """Get list of all open windows with their handles."""
        try:
            windows = ProcessManager.get_window_list()
            return jsonify(windows)
        except Exception as e:
            app.logger.error(f"Error getting window list: {str(e)}")
            return jsonify({'error': 'Failed to get window list'}), 500

    @app.route(f'{Config.API_PREFIX}/kill_process', methods=['POST'])
    def kill_process():
        """Close a window by its handle."""
        try:
            data = request.get_json()
            if not data or 'hwnd' not in data:
                return jsonify({'error': 'Window handle not provided'}), 400
            
            hwnd = int(data['hwnd'])
            ProcessManager.close_window(hwnd)
            return jsonify({'message': f'Window with handle {hwnd} closed successfully'})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            app.logger.error(f"Error closing window: {str(e)}")
            return jsonify({'error': 'Failed to close window'}), 500

    return app

def main():
    """Main application entry point."""
    app = create_app()
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)

if __name__ == '__main__':
    main()

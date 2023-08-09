import socket
from datetime import datetime
from django.shortcuts import render
from .models import LogEntry

def fetch_logs(request):
    HOST = 'localhost'
    PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                log_data = data.decode('utf-8')
                log_entry = process_log_entry(log_data)
                LogEntry.objects.create(**log_entry)
                conn.sendall(b'Log received')

    return render(request, 'logs_received.html')

def correlation_analysis(request):
    num_logs = 100
    logs = generate_sample_logs(num_logs)
    correlation = calculate_correlation(logs)

    context = {
        'correlation': correlation,
        'logs': logs
    }

    return render(request, 'correlation_graph.html', context)


import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from typing import Dict, List, Tuple
import math
import time

def haversine(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    # Вычисляет расстояние между двумя точками на поверхности Земли (в километрах)
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    R = 6371  # Радиус Земли в км
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

import heapq

def dijkstra(graph: Dict[Tuple[float, float], List[Tuple[Tuple[float, float], float, str]]],
             start: Tuple[float, float],
             end: Tuple[float, float]) -> Tuple[List[Tuple[Tuple[float, float], Tuple[float, float]]], float, List[str]]:
    # Приоритетная очередь для хранения (расстояние, узел)
    queue = [(0.0, start)]
    # Словарь для хранения кратчайшего расстояния до каждого узла и предыдущего узла
    distances = {start: 0.0}
    previous_nodes = {start: (None, "")}
    
    # Множество посещённых узлов
    visited = set()
    
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        
        if current_node in visited:
            continue
        visited.add(current_node)
        
        if current_node == end:
            break
            
        if current_node not in graph:
            continue
            
        for neighbor, weight, street_name in graph[current_node]:
            distance = current_distance + weight
            
            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = (current_node, street_name)
                heapq.heappush(queue, (distance, neighbor))
                
    # Восстановление пути
    path_segments = []
    street_names = []
    current = end
    
    if end not in distances:
        return [], float('inf'), []
        
    while previous_nodes[current][0] is not None:
        prev, s_name = previous_nodes[current]
        path_segments.append((prev, current))
        if s_name and s_name not in street_names:
            street_names.append(s_name)
        current = prev
        
    path_segments.reverse()
    street_names.reverse()
    
    return path_segments, distances[end], street_names

def load_graphml(file_path: str):
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {'ns': root.tag.split('}')[0].strip('{')}
    
    nodes = {}
    for node in root.findall('.//ns:node', ns):
        node_id = node.get('id')
        x, y = None, None
        for data in node.findall('ns:data', ns):
            key = data.get('key')
            if key == 'x':
                x = float(data.text)
            elif key == 'y':
                y = float(data.text)
        if x is not None and y is not None:
            nodes[node_id] = (x, y)
            
    graph = {coord: [] for coord in nodes.values()}
    all_edges = []
    
    for edge in root.findall('.//ns:edge', ns):
        source_id = edge.get('source')
        target_id = edge.get('target')
        
        if source_id in nodes and target_id in nodes:
            coord1 = nodes[source_id]
            coord2 = nodes[target_id]
            weight = haversine(coord1, coord2)
            
            street_name = "Unknown"
            for data in edge.findall('ns:data', ns):
                if data.get('key') == 'name' and data.text:
                    street_name = data.text
            
            graph[coord1].append((coord2, weight, street_name))
            graph[coord2].append((coord1, weight, street_name))  # Если граф неориентированный
            all_edges.append((coord1, coord2))
            
    return graph, all_edges

if __name__ == "__main__":
    print("Загрузка графа...")
    # Укажи путь к своему файлу графа Скопье в формате graphml
    graph, all_edges = load_graphml("skopje.graphml")
    print(f"Количество вершин: {len(graph)}")
    print(f"Количество рёбер: {len(all_edges)}")
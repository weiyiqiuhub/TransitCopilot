import geopandas as gpd
from shapely.geometry import LineString
import networkx as nx

class PublicTransportNetwork:
    def __init__(self, shp_file):
        self.data = gpd.read_file(shp_file)
        self.graph = self.build_graph()

    def build_graph(self):
        graph = nx.DiGraph()

        # Add nodes (stops) to the graph
        for _, row in self.data.iterrows():
            stop_id = row['stop_id']
            stop_name = row['stop_name']
            neighborhood = row['neighborhood']
            graph.add_node(stop_id, name=stop_name, neighborhood=neighborhood)

        # Add edges (segments) to the graph
        for _, row in self.data.iterrows():
            route_id = row['route_id']
            stop_ids = row['stop_ids'].split(',')
            geometry = row['geometry']

            for i in range(len(stop_ids) - 1):
                start_stop_id = stop_ids[i]
                end_stop_id = stop_ids[i + 1]
                edge_id = f"{route_id}_{start_stop_id}_{end_stop_id}"

                # Calculate the length of the segment
                segment_geometry = LineString([geometry.coords[i], geometry.coords[i + 1]])
                length = segment_geometry.length

                # Add edge to the graph
                graph.add_edge(start_stop_id, end_stop_id, key=edge_id, route_id=route_id, length=length)

        return graph

    def get_route_segments(self, route_id):
        segments = []
        for u, v, key, data in self.graph.edges(keys=True, data=True):
            if data['route_id'] == route_id:
                start_stop = self.graph.nodes[u]
                end_stop = self.graph.nodes[v]
                segment = {
                    'start_stop_id': u,
                    'start_stop_name': start_stop['name'],
                    'start_stop_neighborhood': start_stop['neighborhood'],
                    'end_stop_id': v,
                    'end_stop_name': end_stop['name'],
                    'end_stop_neighborhood': end_stop['neighborhood'],
                    'segment_id': key,
                    'length': data['length']
                }
                segments.append(segment)
        return segments

    def get_stop_info(self, stop_id):
        if stop_id in self.graph.nodes:
            stop = self.graph.nodes[stop_id]
            return {
                'stop_id': stop_id,
                'stop_name': stop['name'],
                'neighborhood': stop['neighborhood']
            }
        else:
            return None
"""
This is the server file for the distributed tic tac toe game. 
It contains the Berkeley Clock and the Bully Election algorithm.

The Berkeley Clock is a clock synchronization algorithm that uses the network to synchronize clocks.
The Bully Election algorithm is a distributed algorithm for electing a leader in a computer network.
"""
import datetime
import grpc
import threading
import time
from concurrent.futures import ThreadPoolExecutor


import tictactoe_pb2
import tictactoe_pb2_grpc


class BerkeleyClocker(tictactoe_pb2_grpc.BerkeleyClockServicer):
    """
    This class implements the Berkeley Clock algorithm.

    It contains two methods:
    - GetDateTime: returns the current date and time
    - SyncClock: returns the current date and time and the server clock

    The SyncClock method is used to synchronize the client clock with the server clock.
    """

    def GetDateTime(self, request, context):
        # get current date and time
        current_time = datetime.datetime.utcnow()
        # create response
        response = tictactoe_pb2.DateTimeResponse()
        # set date and time
        response.date_time = current_time.strftime(
            "%Y-%m-%d %H:%M:%S.%f")[:-3] + "Z"
        return response

    def SyncClock(self, request, context):
        # get current date and time
        current_time = datetime.datetime.utcnow()
        # create response
        response = tictactoe_pb2.DateTimeResponse()
        # set date and time
        response.server_clock = int(current_time.timestamp() * 1e9)
        # add adjustment
        response.adjust_clock = True
        return response


class BullyElection(tictactoe_pb2_grpc.BullyElectionServicer):
    """
    This class implements the Bully Election algorithm.

    It contains three methods:
    - RegisterNode: registers a new node
    - Heartbeat: sends a heartbeat to the leader
    - GetLeader: returns the current leader

    The RegisterNode method is used to register a new node.
    The Heartbeat method is used to send a heartbeat to the leader.
    The GetLeader method is used to return the current leader.
    """

    HEARTBEAT_INTERVAL_SECONDS = 5
    HEARTBEAT_TIMEOUT_SECONDS = 15

    def __init__(self):
        # initialize nodes
        self.nodes = {}
        # initialize leader
        self.leader = None
        # initialize election lock
        self.election_lock = threading.Lock()
        # start heartbeat thread
        self.heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop)
        # set daemon to exit when main thread exits
        self.heartbeat_thread.daemon = True
        # start thread
        self.heartbeat_thread.start()

    def _heartbeat_loop(self):
        # if no heartbeat is received from the leader within the timeout, start a new election
        while True:
            time.sleep(self.HEARTBEAT_INTERVAL_SECONDS)
            with self.election_lock:
                if not self.leader:
                    # no leader, start election
                    self._start_leader_election()
                else:
                    # check if leader is still alive
                    if self.leader and self.nodes[self.leader] + self.HEARTBEAT_TIMEOUT_SECONDS < time.monotonic():
                        print(f"Leader {self.leader} timed out")
                        self._start_leader_election()

    def RegisterNode(self, request, context):
        node_id = request.node_id
        with self.election_lock:
            self.nodes[node_id] = time.monotonic()
        return tictactoe_pb2.RegisterNodeResponse()

    def Heartbeat(self, request, context):
        node_id = request.node_id
        with self.election_lock:
            self.nodes[node_id] = time.monotonic()
            print(f"Received heartbeat from node {node_id}")
        return tictactoe_pb2.HeartbeatResponse()

    def GetLeader(self, request, context):
        with self.election_lock:
            return tictactoe_pb2.GetLeaderResponse(leader=self.leader)

    def _start_leader_election(self):
        # set leader to None
        self.leader = None
        # send start election request to all nodes
        for node_id in self.nodes:
            self._send_start_election_request(node_id)

    def _send_start_election_request(self, node_id):
        # send start election request to node
        with grpc.insecure_channel(f"[::]:{node_id}") as channel:
            stub = tictactoe_pb2_grpc.BullyElectionStub(channel)
            response = stub.StartElection(tictactoe_pb2.StartElectionRequest())
            # check if node is leader
            if response.leader:
                self.leader = response.leader
                return True
        return False

    def StartElection(self, request, context):
        # start election
        with self.election_lock:
            # check if leader is already set
            if self.leader:
                return tictactoe_pb2.StartElectionResponse(leader=self.leader)
            else:
                # prevent exeption if no nodes are registered
                if not self.nodes:
                    return tictactoe_pb2.StartElectionResponse(leader=None)
                else:
                    self.leader = max(self.nodes.keys())
                for node_id in self.nodes:
                    if node_id != self.leader:
                        self._send_start_election_request(node_id)
                return tictactoe_pb2.StartElectionResponse(leader=self.leader)


def run_server():
    # start server
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    tictactoe_pb2_grpc.add_BerkeleyClockServicer_to_server(
        BerkeleyClocker(), server)
    tictactoe_pb2_grpc.add_BullyElectionServicer_to_server(
        BullyElection(), server)
    server.add_insecure_port("[::]:20048")
    print("Server CONNECTED to port 20048...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    run_server()

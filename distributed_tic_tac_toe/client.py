"""
This is the client code for the distributed tic-tac-toe game.
It contains the Berkeley Clock and the Bully Election algorithm.

The Berkeley Clock is a clock synchronization algorithm that uses the network to synchronize clocks.
The Bully Election algorithm is a distributed algorithm for electing a leader in a computer network.

The Berkeley Clock is used to synchronize the client clock with the server clock.
The Bully Election algorithm is used to elect a leader in the distributed system.
"""

from concurrent import futures
import sys
import grpc
import threading
import time
import datetime

import tictactoe_pb2
import tictactoe_pb2_grpc

from tictactoe_pb2 import ClockAdjustmentRequest


class BerkeleyClockClient:
    """
    This class implements the Berkeley Clock algorithm.

    It contains two methods:
    - GetDateTime: returns the current date and time
    - SyncClock: returns the current date and time and the server clock

    The SyncClock method is used to synchronize the client clock with the server clock.
    """

    def __init__(self, channel):
        self.stub = tictactoe_pb2_grpc.BerkeleyClockStub(channel)

    def get_datetime(self):
        request = tictactoe_pb2.DateTimeRequest()
        response = self.stub.GetDateTime(request)
        return response.date_time

    def SyncClock(self, request):
        response = self.stub.SyncClock(request)
        return response


class ElectionClient:
    """
    This class implements the Bully Election algorithm.

    It contains three methods:
    - RegisterNode: registers a new node
    - Heartbeat: sends a heartbeat to the leader
    - GetLeader: returns the current leader

    """

    def __init__(self, channel, node_id):
        self.stub = tictactoe_pb2_grpc.BullyElectionStub(channel)
        self.node_id = node_id

    def get_leader(self):
        request = tictactoe_pb2.GetLeaderRequest()
        response = self.stub.GetLeader(request)
        return response.leader

    def StartElection(self):
        request = tictactoe_pb2.StartElectionRequest(
            node_id=self.node_id)
        response = self.stub.StartElection(request)
        return response


def sync_clock(client, stop_event):
    """
    This function synchronizes the client clock with the server clock.
    """
    while not stop_event.is_set():
        time.sleep(5)
        adjustment = 0
        start_time = time.time()
        server_clock = client.SyncClock(
            ClockAdjustmentRequest(adjustment=adjustment)).server_clock
        end_time = time.time()
        client_clock = int(datetime.datetime.utcnow().timestamp() * 1e9)
        estimated_server_clock = server_clock + int(
            (end_time - start_time) * 1e9 / 2)
        adjustment = estimated_server_clock - client_clock
        print("Clock adjustment: ", adjustment)
        client_time = datetime.datetime.utcnow() + datetime.timedelta(
            microseconds=adjustment / 1000)
        print("Client time: ", client_time)


def send_heartbeat(election_client, stop_event):
    """
    This function sends a heartbeat to the leader.
    """
    while not stop_event.is_set():
        time.sleep(5)
        election_client.stub.Heartbeat(
            tictactoe_pb2.HeartbeatRequest(node_id=election_client.node_id))


def start_election():
    """
    This function starts an election.
    """
    with grpc.insecure_channel("[::]:20048") as channel:
        client = ElectionClient(channel, node_id)
        client.StartElection()


def get_leader():
    """
    This function returns the current leader.
    """

    with grpc.insecure_channel("[::]:20048") as channel:
        client = ElectionClient(channel, node_id)
        leader = client.get_leader()
        print(f"Current leader: {leader}")


def run_client(node_id):
    """

    This function runs the client.
    It contains the following steps:
    - Register the node
    - Synchronize the clock
    - Start an election
    - Send a heartbeat
    """
    with grpc.insecure_channel("localhost:20048") as channel:
        stop_event = threading.Event()
        while not stop_event.is_set():
            try:
                clock_client = BerkeleyClockClient(channel)
                clock_thread = threading.Thread(
                    target=sync_clock, args=(clock_client, stop_event))
                clock_thread.start()

                election_client = ElectionClient(channel, node_id)
                leader = election_client.get_leader()
                print(f"Current leader: {leader}")
                if leader == node_id:
                    print("I am the leader")

                else:
                    print("I am not the leader")

                heartbeat_thread = threading.Thread(
                    target=send_heartbeat, args=(election_client, stop_event))
                heartbeat_thread.start()

                # If there is no leader, start an election
                if not leader:
                    election_thread = threading.Thread(
                        target=start_election, args=())
                    election_thread.start()

                time.sleep(5)

            except grpc.RpcError as e:
                print(f"Error: {e}")
                time.sleep(1)


if __name__ == "__main__":
    # Get the node id from the command line
    node_id = sys.argv[1]
    # Start the client
    client_thread = threading.Thread(target=run_client, args=(node_id,))
    client_thread.start()
    client_thread.join()

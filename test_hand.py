import unittest
from unittest.mock import patch, MagicMock
import numpy as np

# Import LeapNode class from your module, assuming leap_hand_node.py
# from leap_hand_node import LeapNode
# For this example, assume LeapNode is already in the namespace
from main import LeapNode

import leap_hand_utils.leap_hand_utils as lhu

class TestLeapNode(unittest.TestCase):
    @patch('leap_hand_utils.dynamixel_client.DynamixelClient')
    def setUp(self, mock_dxl_client_class):
        # Setup the mock DynamixelClient instance
        self.mock_dxl_client = MagicMock()
        mock_dxl_client_class.return_value = self.mock_dxl_client

        # Instantiate LeapNode (this will use mocked DynamixelClient)
        self.leap_node = LeapNode()

    def test_initialization(self):
        # Check if connect() called once
        self.mock_dxl_client.connect.assert_called_once()

        # Check if torque enabled called with all motors
        self.mock_dxl_client.set_torque_enabled.assert_called_once_with(self.leap_node.motors, True)

        # Check if initial position was written
        self.mock_dxl_client.write_desired_pos.assert_called_with(self.leap_node.motors, self.leap_node.curr_pos)

    def test_set_leap(self):
        test_pose = np.linspace(0, 1, 16)
        self.leap_node.set_leap(test_pose)
        self.assertTrue(np.allclose(self.leap_node.curr_pos, test_pose))
        self.mock_dxl_client.write_desired_pos.assert_called_with(self.leap_node.motors, test_pose)

    def test_set_allegro(self):
        test_pose = np.zeros(16)
        # Patch allegro_to_LEAPhand to track conversion
        with patch('leap_hand_utils.leap_hand_utils.allegro_to_LEAPhand', wraps=lhu.allegro_to_LEAPhand) as mock_convert:
            self.leap_node.set_allegro(test_pose)
            mock_convert.assert_called_once_with(test_pose, zeros=False)
            # Check current pos updated with converted value
            converted_pose = lhu.allegro_to_LEAPhand(test_pose, zeros=False)
            self.assertTrue(np.allclose(self.leap_node.curr_pos, converted_pose))
            self.mock_dxl_client.write_desired_pos.assert_called_with(self.leap_node.motors, converted_pose)

    def test_set_ones(self):
        test_pose = np.zeros(16)
        with patch('leap_hand_utils.leap_hand_utils.sim_ones_to_LEAPhand', wraps=lhu.sim_ones_to_LEAPhand) as mock_convert:
            self.leap_node.set_ones(test_pose)
            mock_convert.assert_called_once_with(test_pose)
            converted_pose = lhu.sim_ones_to_LEAPhand(test_pose)
            self.assertTrue(np.allclose(self.leap_node.curr_pos, converted_pose))
            self.mock_dxl_client.write_desired_pos.assert_called_with(self.leap_node.motors, converted_pose)

    def test_read_methods(self):
        # Setup return values
        pos = np.arange(16)
        vel = np.arange(16)*0.1
        cur = np.arange(16)*0.01

        self.mock_dxl_client.read_pos.return_value = pos
        self.mock_dxl_client.read_vel.return_value = vel
        self.mock_dxl_client.read_cur.return_value = cur
        self.mock_dxl_client.read_pos_vel.return_value = (pos, vel)
        self.mock_dxl_client.read_pos_vel_cur.return_value = (pos, vel, cur)

        self.assertTrue(np.array_equal(self.leap_node.read_pos(), pos))
        self.assertTrue(np.array_equal(self.leap_node.read_vel(), vel))
        self.assertTrue(np.array_equal(self.leap_node.read_cur(), cur))
        self.assertEqual(self.leap_node.pos_vel(), (pos, vel))
        self.assertEqual(self.leap_node.pos_vel_eff_srv(), (pos, vel, cur))

if __name__ == '__main__':
    unittest.main()

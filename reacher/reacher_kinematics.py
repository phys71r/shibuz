from cmath import cos, sin
import math
from ntpath import join
import numpy as np
import copy

HIP_OFFSET = 0.0335
L1 = 0.08  # length of link 1
L2 = 0.11  # length of link 2


def calculate_forward_kinematics_robot(joint_angles):
    """Calculate xyz coordinates of end-effector given joint angles.

    Use forward kinematics equations to calculate the xyz coordinates of the end-effector
    given some joint angles.

    Args:
      joint_angles: numpy array of 3 elements [TODO names]. Numpy array of 3 elements.
    Returns:
      xyz coordinates of the end-effector in the arm frame. Numpy array of 3 elements.
    """
    # TODO for students: Implement this function. ~25-35 lines of code.
    rc = np.array([0,
                   0,
                   L2])

    rotate_bc = np.array([[math.cos(joint_angles[2]), 0, -math.sin(joint_angles[2])],
                          [0, 1,                          0],
                          [math.sin(joint_angles[2]), 0,
                           math.cos(joint_angles[2])]
                          ])

    rb = np.add([0, 0, L1], np.matmul(rotate_bc, rc))

    rotate_ab = np.array([[math.cos(joint_angles[1]), 0, -math.sin(joint_angles[1])],
                          [0, 1,                          0],
                          [math.sin(joint_angles[1]), 0,
                           math.cos(joint_angles[1])]
                          ])

    ra = np.add([0, -HIP_OFFSET, 0], np.matmul(rotate_ab, rb))

    rotate_na = np.array([[math.cos(-joint_angles[0]), -math.sin(-joint_angles[0]), 0],
                          [math.sin(-joint_angles[0]),
                           math.cos(-joint_angles[0]), 0],
                          [0,                     0,      1]
                          ])

    rn = np.matmul(rotate_na, ra)
    return rn


def ik_cost(end_effector_pos, guess):
    """Calculates the inverse kinematics loss.

    Calculate the Euclidean distance between the desired end-effector position and
    the end-effector position resulting from the given 'guess' joint angles.

    Args:
      end_effector_pos: desired xyz coordinates of end-effector. Numpy array of 3 elements.
      guess: guess at joint angles to achieve desired end-effector position. Numpy array of 3 elements.
    Returns:
      Euclidean distance between end_effector_pos and guess. Returns float.
    """
    # TODO for students: Implement this function. ~1-5 lines of code.
    euclid_dist_vector = np.subtract(
        calculate_forward_kinematics_robot(guess), end_effector_pos)
    euclid_dist = np.sqrt(
        euclid_dist_vector[0]**2 + euclid_dist_vector[1]**2 + euclid_dist_vector[2]**2)
    return euclid_dist

    # cost = 0.0
    # raise cost


def calculate_jacobian(joint_angles):
    """Calculate the jacobian of the end-effector position wrt joint angles.

    Calculate the jacobian, which is a matrix of the partial derivatives
    of the forward kinematics with respect to the joint angles 
    arranged as such:

    dx/dtheta1 dx/dtheta2 dx/dtheta3
    dy/dtheta1 dy/dtheta2 dy/dtheta3
    dz/dtheta1 dz/dtheta2 dz/dtheta3

    Args:
      joint_angles: joint angles of robot arm. Numpy array of 3 elements.

    Returns:
      Jacobian matrix. Numpy 3x3 array.
    """
    # TODO for students: Implement this function. ~5-10 lines of code.
    angle_offset = 0.001

    no_offset = calculate_forward_kinematics_robot(joint_angles)

    theta1_offset = calculate_forward_kinematics_robot(np.array([joint_angles[0] + angle_offset,
                                                                 joint_angles[1],
                                                                 joint_angles[2]]))
    theta2_offset = calculate_forward_kinematics_robot(np.array([joint_angles[0],
                                                                 joint_angles[1] +
                                                                 angle_offset,
                                                                 joint_angles[2]]))
    theta3_offset = calculate_forward_kinematics_robot(np.array([joint_angles[0],
                                                                 joint_angles[1],
                                                                 joint_angles[2] + angle_offset]))

    jacobian_col1 = (np.add(theta1_offset, -no_offset)) / angle_offset
    jacobian_col2 = (np.add(theta2_offset, -no_offset)) / angle_offset
    jacobian_col3 = (np.add(theta3_offset, -no_offset)) / angle_offset

    jacobian = np.transpose(
        np.array([jacobian_col1, jacobian_col2, jacobian_col3]))

    return jacobian


def calculate_inverse_kinematics(end_effector_pos, guess):
    """Calculates joint angles given desired xyz coordinates.

    Use gradient descent to minimize the inverse kinematics loss function. The
    joint angles that minimize the loss function are the joint angles that give 
    the smallest error from the actual resulting end-effector position to the
    desired end-effector position. You should use the jacobain function
    you wrote above.

    Args:
      end_effector_pos: Desired xyz coordinates of end-effector. Numpy array of 3 elements.
      guess: Guess at joint angles that achieve desired end-effector position. Numpy array of 3 elements.
    Returns:
      Joint angles that correspond to given desired end-effector position. Numpy array with 3 elements.
    """
    # TODO for students: Implement this function. ~10-20 lines of code.
    alpha = 0.1
    epsilon = 0.01
    cost = 1000
    while(cost > epsilon):
        jacobian = calculate_jacobian(guess)
        euclid_dist_vector = np.subtract(
            calculate_forward_kinematics_robot(guess), end_effector_pos)
        cost_grad = np.matmul(np.transpose(jacobian), euclid_dist_vector)
        cost = ik_cost(end_effector_pos, guess)
        guess = guess - alpha * cost_grad

    return guess

# target = [0.05, 0.07, 0.01]
# angles = calculate_inverse_kinematics(target, [0, 0, 0])
# print(angles)
# coords = calculate_forward_kinematics_robot(angles)
# print(coords)
# dist_vector = np.subtract(coords, target)
# dist = np.sqrt(np.dot(dist_vector, dist_vector))
# print(dist)

import React, { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState({ name: "", email: "", telephonenumber: "", author: "Staff" });

  // Fetch all users
  useEffect(() => {
    fetch("http://localhost:5000/users")
      .then((response) => response.json())
      .then((data) => setUsers(data.users))
      .catch((error) => console.error("Error fetching users:", error));
  }, []);


  const handleChange = (e) => {
    setNewUser({ ...newUser, [e.target.name]: e.target.value });
  };


  const handleAddUser = () => {
    fetch("http://localhost:5000/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newUser),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          setUsers([...users, { userid: data.userid, ...newUser }]); 
          setNewUser({ name: "", email: "", telephonenumber: "", author: "Staff" });
        }
      })
      .catch((error) => console.error("Error adding user:", error));
  };

  // Delete user
  const handleDeleteUser = (userid) => {
    fetch(`http://localhost:5000/users/${userid}`, { method: "DELETE" })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          setUsers(users.filter((user) => user.userid !== userid)); 
        }
      })
      .catch((error) => console.error("Error deleting user:", error));
  };

  return (
    <div className="flex inventory-container">
      <Sidebar />
      <div className="flex-1 ml-60 p-5">
        <h2>User Management</h2>

        {/* Add User Form */}
        <div className="form-container">
          <input type="text" name="name" placeholder="Name" value={newUser.name} onChange={handleChange} />
          <input type="email" name="email" placeholder="Email" value={newUser.email} onChange={handleChange} />
          <input type="text" name="telephonenumber" placeholder="Phone" value={newUser.telephonenumber} onChange={handleChange} />
          <select name="author" value={newUser.author} onChange={handleChange}>
            <option value="Staff">Staff</option>
            <option value="Admin">Admin</option>
          </select>
          <button onClick={handleAddUser}>Add User</button>
        </div>

        {/* Users Table */}
        <table className="user-table">
          <thead>
            <tr>
              <th>User ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Role</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.length > 0 ? (
              users.map((user) => (
                <tr key={user.userid}>
                  <td>{user.userid}</td>
                  <td>{user.name}</td>
                  <td>{user.email}</td>
                  <td>{user.telephonenumber}</td>
                  <td>{user.author}</td>
                  <td>
                    <button className="delete-btn" onClick={() => handleDeleteUser(user.userid)}>Delete</button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6">No users found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default UserManagement;

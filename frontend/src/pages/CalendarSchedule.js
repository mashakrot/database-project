import React, { useState, useEffect } from 'react';
import { Calendar } from 'react-calendar';
import Sidebar from "../components/Sidebar";
import 'react-calendar/dist/Calendar.css';
import '../css/CalendarSchedule.css';  

const CalendarSchedule = () => {
  const [schedules, setSchedules] = useState([]);
  const [date, setDate] = useState(new Date());
  const [editingShift, setEditingShift] = useState(null); 
  const [newShift, setNewShift] = useState({ shiftdate: "", timestart: "", timeend: "" });
  const [searchFilters, setSearchFilters] = useState({ shiftdate: '', approvalstatus: '', userid: '' });

  useEffect(() => {
    fetch('http://localhost:5000/get_schedules', { method: 'GET' }) 
      .then((response) => response.json())
      .then((data) => {
        if (data.status === 'success') {
          setSchedules(data.schedules); 
        }
      })
      .catch((error) => console.log(error));
  }, []);
  

  // Function to get shifts for a particular day
  const getShiftsForDay = (day) => {
    const dayStr = day.toISOString().split('T')[0]; 
    return schedules.filter(
      (schedule) => schedule.shiftdate === dayStr
    );
  };

  // Function to get the color based on approval status
  const getStatusColor = (status) => {
    switch (status) {
      case 'Approved':
        return 'approved';
      case 'Pending':
        return 'pending';
      case 'Rejected':
        return 'rejected';
      default:
        return 'gray';
    }
  };

  const renderShiftBlocks = (day) => {
    const shiftsForDay = getShiftsForDay(day);
    return shiftsForDay.map((shift) => (
      <div
        key={shift.scheduleid}
        className={`shift-block ${getStatusColor(shift.approvalstatus)}`}
      >
        <p className="user-id">{shift.userid}</p>
        <p className="shift-time">
          {shift.timestart} - {shift.timeend}
        </p>
        <span className="status">{shift.approvalstatus}</span>
      </div>
    ));
  };

  // Handle new shift form submission
  const handleAddShift = () => {
    const newShiftData = {
      ...newShift,
      approvalstatus: "Pending",
    };

    fetch('http://localhost:5000/add_shift', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newShiftData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          setSchedules([...schedules, data.shift]);  
        }
      })
      .catch((error) => console.log(error));
  };

  //  Editing Shift
  const handleEditShift = () => {
    if (!editingShift) return;

    const updatedShiftData = {
      ...editingShift,
      timestart: newShift.timestart || editingShift.timestart,
      timeend: newShift.timeend || editingShift.timeend,
    };

    fetch('http://localhost:5000/edit_shift', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updatedShiftData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          setSchedules(schedules.map((shift) => (shift.scheduleid === data.shift.scheduleid ? data.shift : shift)));
        }
      })
      .catch((error) => console.log(error));
  };

  //  Approve/Reject Shift
  const handleChangeShiftStatus = (status) => {
    if (!editingShift) return;

    const updatedShiftData = { ...editingShift, approvalstatus: status };

    fetch('http://localhost:5000/change_shift_status', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updatedShiftData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          setSchedules(schedules.map((shift) => (shift.scheduleid === data.shift.scheduleid ? data.shift : shift)));
        }
      })
      .catch((error) => console.log(error));
  };

  return (
    <div className="p-6 w-full container">
      <Sidebar />
      <div className="flex-1 ml-60 p-5">
        <div className="p-6 w-full">

          <div className="content">
            <div className="calendar-container">
              <h2 className="calendar-title">Staff Schedule Calendar</h2>

              <div className="calendar">
                <Calendar
                  onChange={setDate}
                  value={date}
                  tileContent={({ date, view }) => {
                    if (view === 'month') {
                      return (
                        <div className="shift-container">
                          {renderShiftBlocks(date)}
                        </div>
                      );
                    }
                    return null;
                  }}
                />
              </div>
            </div>

            {/* Add a New Shift Form */}
            <div className="shift-form">
              <h3 className="form-title">Add a New Shift</h3>
              <input
                type="date"
                value={newShift.shiftdate}
                onChange={(e) => setNewShift({ ...newShift, shiftdate: e.target.value })}
                className="form-input"
              />
              <div className="time-inputs">
                <input
                  type="time"
                  value={newShift.timestart}
                  onChange={(e) => setNewShift({ ...newShift, timestart: e.target.value })}
                  className="form-input"
                />
                <input
                  type="time"
                  value={newShift.timeend}
                  onChange={(e) => setNewShift({ ...newShift, timeend: e.target.value })}
                  className="form-input"
                />
              </div>
              <button onClick={handleAddShift} className="form-button">Add Shift</button>
            </div>
          </div>

          {/* Edit Shift Form */}
          {editingShift && (
            <div className="edit-shift-form">
              <h3 className="form-title">Edit Shift</h3>
              <div className="time-inputs">
                <input
                  type="time"
                  defaultValue={editingShift.timestart}
                  onChange={(e) => setNewShift({ ...newShift, timestart: e.target.value })}
                  className="form-input"
                />
                <input
                  type="time"
                  defaultValue={editingShift.timeend}
                  onChange={(e) => setNewShift({ ...newShift, timeend: e.target.value })}
                  className="form-input"
                />
              </div>
              <button onClick={handleEditShift} className="form-button save">Save Changes</button>
              <button onClick={() => handleChangeShiftStatus("Approved")} className="form-button approve">Approve Shift</button>
              <button onClick={() => handleChangeShiftStatus("Rejected")} className="form-button reject">Reject Shift</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CalendarSchedule;

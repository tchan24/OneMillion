import React, { useState, useEffect } from 'react';
import { getResources, addResource, checkoutResources, checkinResources } from '../api';

const ResourceManagement = () => {
  const [resources, setResources] = useState([]);
  const [newResource, setNewResource] = useState({ name: '', capacity: 0 });
  const [checkoutData, setCheckoutData] = useState({ hw_set: '', quantity: 0 });

  useEffect(() => {
    fetchResources();
  }, []);

  const fetchResources = async () => {
    try {
      const response = await getResources();
      setResources(response.data);
    } catch (error) {
      console.error('Error fetching resources:', error);
    }
  };

  const handleAddResource = async (e) => {
    e.preventDefault();
    try {
      await addResource(newResource);
      setNewResource({ name: '', capacity: 0 });
      fetchResources();
    } catch (error) {
      console.error('Error adding resource:', error);
    }
  };

  const handleCheckout = async (e) => {
    e.preventDefault();
    try {
      await checkoutResources(checkoutData.hw_set, checkoutData.quantity);
      setCheckoutData({ hw_set: '', quantity: 0 });
      fetchResources();
    } catch (error) {
      console.error('Error checking out resource:', error);
    }
  };

  const handleCheckin = async (e) => {
    e.preventDefault();
    try {
      await checkinResources(checkoutData.hw_set, checkoutData.quantity);
      setCheckoutData({ hw_set: '', quantity: 0 });
      fetchResources();
    } catch (error) {
      console.error('Error checking in resource:', error);
    }
  };

  return (
    <div>
      <h2>Resource Management</h2>
      <form onSubmit={handleAddResource}>
        <input
          type="text"
          placeholder="Resource Name"
          value={newResource.name}
          onChange={(e) => setNewResource({ ...newResource, name: e.target.value })}
        />
        <input
          type="number"
          placeholder="Capacity"
          value={newResource.capacity}
          onChange={(e) => setNewResource({ ...newResource, capacity: parseInt(e.target.value) })}
        />
        <button type="submit">Add Resource</button>
      </form>
      <form onSubmit={handleCheckout}>
        <input
          type="text"
          placeholder="Hardware Set"
          value={checkoutData.hw_set}
          onChange={(e) => setCheckoutData({ ...checkoutData, hw_set: e.target.value })}
        />
        <input
          type="number"
          placeholder="Quantity"
          value={checkoutData.quantity}
          onChange={(e) => setCheckoutData({ ...checkoutData, quantity: parseInt(e.target.value) })}
        />
        <button type="submit">Checkout</button>
        <button onClick={handleCheckin}>Check In</button>
      </form>
      <ul>
        {resources.map(resource => (
          <li key={resource._id}>{resource.name} - Available: {resource.available}/{resource.capacity}</li>
        ))}
      </ul>
    </div>
  );
};

export default ResourceManagement;
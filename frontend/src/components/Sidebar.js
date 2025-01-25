import React from "react";

const Sidebar = ({ modules, onModuleSelect }) => {
  return (
    <div style={{ width: "20%", background: "#f0f0f0", height: "100vh", padding: "1rem" }}>
      <ul>
        {modules.map((module) => (
          <li key={module.id} onClick={() => onModuleSelect(module)}>
            {module.name}
          </li>
        ))}
        
      </ul>
    </div>
  );
};

export default Sidebar;

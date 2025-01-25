import React, { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import TopBar from "./components/TopBar";
import MainArea from "./components/MainArea";
import axios from "axios";

const App = () => {
  const [modules, setModules] = useState([]);
  const [selectedModule, setSelectedModule] = useState(null);
  const [openedModules, setOpenedModules] = useState([]); // Oprava: Inicializace openedModules

  const handleModuleSelect = (module) => {
    setSelectedModule(module);
    if (!openedModules.find((mod) => mod.id === module.id)) {
      setOpenedModules([...openedModules, module]);
    }
  }; // Oprava: Správné uzavření funkce

  useEffect(() => {
    // Načtení modulů z backendu
    axios
      .get("http://localhost:8000/modules")
      .then((response) => {
        setModules(response.data);
      })
      .catch((error) => {
        console.error("Error fetching modules:", error);
      });
  }, []); // Oprava: Přidání prázdného pole závislostí

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      <TopBar openedModules={openedModules} />
      <div style={{ display: "flex", flex: 1 }}>
        <Sidebar modules={modules} onModuleSelect={handleModuleSelect} />
        <MainArea selectedModule={selectedModule} />
      </div>
    </div>
  );
};

export default App;

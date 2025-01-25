import React, { useState, useEffect } from "react";

const MainArea = ({ selectedModule }) => {
  const [ModuleComponent, setModuleComponent] = useState(null);

  useEffect(() => {
    if (selectedModule) {
      const loadModule = async () => {
        try {
          const module = await import(`./modules/${selectedModule.name}`);
          setModuleComponent(() => module.default);
        } catch (error) {
          console.error(`Modul ${selectedModule.name} nebyl nalezen.`, error);
          setModuleComponent(null);
        }
      };

      loadModule();
    }
  }, [selectedModule]);

  if (!selectedModule) {
    return <div style={{ padding: "20px" }}>Vyberte modul z menu vlevo.</div>;
  }

  return (
    <div style={{ padding: "20px", flex: 1 }}>
      {ModuleComponent ? (
        <React.Suspense fallback={<div>Načítání modulu...</div>}>
          <ModuleComponent />
        </React.Suspense>
      ) : (
        <div>
          Modul <strong>{selectedModule.name}</strong> není dostupný.
        </div>
      )}
    </div>
  );
};

export default MainArea;

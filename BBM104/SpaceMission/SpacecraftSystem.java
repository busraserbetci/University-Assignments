import java.util.*;

public abstract class SpacecraftSystem {
    protected double energyConsumption; // Energy consumption of the system

    public SpacecraftSystem(double energyConsumption) {
        this.energyConsumption = energyConsumption;
    }

    // Abstract method to activate the system
    public abstract boolean activate();
}

class PropulsionSystem extends SpacecraftSystem {
    private double fuelLevel; // Current fuel level
    private double fuelConsumptionRate; // Rate at which fuel is consumed

    public PropulsionSystem(double energy, double fuel, double consumptionRate) {
        super(energy);
        this.fuelLevel = fuel;
        this.fuelConsumptionRate = consumptionRate;
    }

    // Method to calculate fuel consumption based on distance
    public double calculateFuelConsumption(double distance) {
        double requiredFuel = distance * fuelConsumptionRate;
        return requiredFuel; // Returns the required fuel for the given distance
    }

    // Method to check if there is enough fuel to complete the mission
    public boolean checkFuel(double requiredFuel) {
        if (fuelLevel >= requiredFuel) {
            fuelLevel -= requiredFuel; // Decrease fuel level if enough fuel is available
            return true;
        } else {
            return false; // Not enough fuel
        }
    }

    @Override
    public boolean activate() {
        System.out.println("Propulsion System is now active.");
        System.out.println("Propulsion system is ready for launch.");
        return true;
    }

    // Method to display fuel status
    public void displayFuelStatus() {

        System.out.println("Propulsion System Status: Operating at " + String.format("%.1f", fuelLevel) + "% fuel");
        System.out.println("Fuel Level: " + String.format("%.1f", fuelLevel));
    }

    // Method to put the propulsion system on standby
    public void standby() {
        System.out.println("Propulsion System is now standby.");
    }

    public double getFuelLevel() {
        return fuelLevel;
    }
}


class NavigationSystem extends SpacecraftSystem {
    protected double currentLatitude; // Current latitude of the spacecraft
    protected double currentLongitude; // Current longitude of the spacecraft

    public NavigationSystem(double energyConsumption, double currentLatitude, double currentLongitude) {
        super(energyConsumption);
        this.currentLatitude = currentLatitude;
        this.currentLongitude = currentLongitude;
    }

    // Method to calculate the distance to a target using the Haversine formula
    public double calculateDistanceToTarget(double targetLatitude, double targetLongitude) {
        final int R = 6371; // Radius of the Earth in kilometers

        // Convert latitude and longitude from degrees to radians
        double latDistance = Math.toRadians(targetLatitude - currentLatitude);
        double lonDistance = Math.toRadians(targetLongitude - currentLongitude);

        // Apply Haversine formula
        double a = Math.sin(latDistance / 2) * Math.sin(latDistance / 2) +
                Math.cos(Math.toRadians(currentLatitude)) * Math.cos(Math.toRadians(targetLatitude)) *
                        Math.sin(lonDistance / 2) * Math.sin(lonDistance / 2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

        double distance = R * c;

        return distance;
    }

    @Override
    public boolean activate() {
        System.out.println("Navigation System is now active.");
        System.out.println("Navigation system activated and stabilizing environment.");
        return true;
    }

    // Method to put the navigation system on standby
    public void standby() {
        System.out.println("Navigation System is now standby.");
    }

    public double getCurrentLatitude() {
        return currentLatitude;
    }

    public void setCurrentLatitude(double currentLatitude) {
        this.currentLatitude = currentLatitude;
    }

    public double getCurrentLongitude() {
        return currentLongitude;
    }

    public void setCurrentLongitude(double currentLongitude) {
        this.currentLongitude = currentLongitude;
    }
}

class LifeSupportSystem extends SpacecraftSystem {
    private double oxygenLevel; // Current oxygen level
    private double oxygenMultiplier; // Multiplier to calculate oxygen requirements based on temperature
    private double temperature; // Current temperature in the spacecraft

    public LifeSupportSystem(double energy, double oxygen, double temperature, double multiplier) {
        super(energy);  // Calling the superclass constructor
        this.oxygenLevel = oxygen;
        this.oxygenMultiplier = multiplier;
        this.temperature = temperature;
    }

    // Method to activate the system based on mission temperature and duration
    public boolean activateSystem(double missionTemperature, double missionDuration) {
        double spacecraftTemperature = this.temperature;

        double temperatureDifference = Math.abs(missionTemperature - spacecraftTemperature);

        double requiredOxygen = temperatureDifference * this.oxygenMultiplier * missionDuration;

        if (this.oxygenLevel >= requiredOxygen) {
            this.oxygenLevel -= requiredOxygen; // Decrease oxygen level if sufficient oxygen is available
            return true;
        } else {
            return false; // Not enough oxygen
        }
    }

    @Override
    public boolean activate() {
        System.out.println("Life Support System is now active.");
        System.out.println("Life support system activated and stabilizing environment.");
        return true;
    }

    // Method to display life support status
    public void displayLifeSupportStatus() {
        System.out.println("Life Support System Status: Oxygen Level: " + String.format("%.1f", oxygenLevel) + "%, Temperature: 19.0°C");
    }

    // Method to put the life support system on standby
    public void standby() {
        System.out.println("Life Support System is now standby.");
    }

    public double getOxygenLevel() {
        return oxygenLevel;
    }

    public double getOxygenMultiplier() {
        return oxygenMultiplier;
    }

    public double getCurrentTemperature() {
        return this.temperature;
    }
}

class Spacecraft {
    private String name; // Name of the spacecraft
    private List<SpacecraftSystem> systems; // List of spacecraft systems
    private Mission mission; // The mission assigned to the spacecraft
    private double totalEnergy; // Total energy available for the spacecraft

    public Spacecraft(String name, List<SpacecraftSystem> systems, Mission mission, double totalEnergy) {
        this.name = name;
        this.systems = systems;
        this.mission = mission;
        this.totalEnergy = totalEnergy;
    }

    // Method to start the mission
    public void startMission() {
        // Retrieving individual systems from the list
        PropulsionSystem propSys = (PropulsionSystem) systems.get(0);
        LifeSupportSystem lifeSupportSystem = (LifeSupportSystem) systems.get(1);
        NavigationSystem navSys = (NavigationSystem) systems.get(2);

        // Activate all systems
        propSys.activate();
        lifeSupportSystem.activate();
        navSys.activate();

        // Calculate necessary mission parameters like fuel and oxygen requirements
        double tempDifference = mission.temperature - lifeSupportSystem.getCurrentTemperature();
        double distance = navSys.calculateDistanceToTarget(mission.latitude, mission.longitude);
        double requiredFuel = propSys.calculateFuelConsumption(distance);
        double requiredOxygen = mission.temperature * lifeSupportSystem.getOxygenMultiplier() * mission.duration;

        // Check if there is enough fuel for the mission
        if (!propSys.checkFuel(requiredFuel)) {
            System.out.println("Cannot perform spaceflight, fuel level is not enough!");
            propSys.standby();
            lifeSupportSystem.standby();
            navSys.standby();

            if (mission instanceof ExploreMission) {
                System.out.println("Explore mission start failed");
            } else if (mission instanceof SatelliteMission) {
                System.out.println("Satellite mission start failed");
            } else if (mission instanceof SupplyMission) {
                System.out.println("Supply mission start failed");
            }
            return;
        }

        // Check if there is enough oxygen for the mission
        if (!lifeSupportSystem.activateSystem(mission.temperature, mission.duration)) {
            System.out.println("Cannot perform spaceflight, oxygen level is not enough!");
            propSys.standby();
            lifeSupportSystem.standby();
            navSys.standby();

            if (mission instanceof ExploreMission) {
                System.out.println("Explore mission start failed");
            } else if (mission instanceof SatelliteMission) {
                System.out.println("Satellite mission start failed");
            } else if (mission instanceof SupplyMission) {
                System.out.println("Supply mission start failed");
            }
            return;
        }

        System.out.println("All systems active");
        mission.performMission();

        System.out.println("Spacecraft Status: " + name);
        System.out.printf("Propulsion System Status: Operating at %.1f%% fuel\n", propSys.getFuelLevel());
        System.out.println("Fuel Level: " + propSys.getFuelLevel());
        System.out.println("Life Support System Status: Oxygen Level: " + String.format("%.1f", lifeSupportSystem.getOxygenLevel()) + "%, Temperature: " + mission.temperature + "\u00B0C");
        System.out.println("Navigation System Status: Active");
        System.out.println("Current Latitude: " + navSys.currentLatitude + " CurrentLongitude: " + navSys.currentLongitude);

        if (mission instanceof ExploreMission) {
            System.out.println("Explore mission is ended");
        } else if (mission instanceof SatelliteMission) {
            System.out.println("Satellite retrieval mission is ended");
        } else if (mission instanceof SupplyMission) {
            System.out.println("Supply mission is ended");
        }
    }
}

// Abstract base class for a mission
public abstract class Mission {
    protected String name;
    protected double latitude;
    protected double longitude;
    protected double duration;
    protected double temperature;

    // Constructor to initialize the mission details
    public Mission(String name, double lat, double lon, double duration, double temp) {
        this.name = name;
        this.latitude = lat;
        this.longitude = lon;
        this.duration = duration;
        this.temperature = temp;
    }

    // Abstract method that must be implemented by subclasses to perform the mission
    public abstract void performMission();
}

// Concrete class for an Exploration mission
class ExploreMission extends Mission {
    // Constructor to initialize the mission details specific to ExploreMission
    public ExploreMission(String name, double lat, double lon, double duration, double temp) {
        super(name, lat, lon, duration, temp); // Call the constructor of the parent class
    }

    @Override
    public void performMission() {
        System.out.println("Exploration mission started!");
    }
}

// Concrete class for a Satellite Retrieval mission
class SatelliteMission extends Mission {
    // Constructor to initialize the mission details specific to SatelliteMission
    public SatelliteMission(String name, double lat, double lon, double duration, double temp) {
        super(name, lat, lon, duration, temp); // Call the constructor of the parent class
    }

    @Override
    public void performMission() {
        System.out.println("Satellite retrieval mission started!");
    }
}

// Concrete class for a Supply mission
class SupplyMission extends Mission {
    // Constructor to initialize the mission details specific to SupplyMission
    public SupplyMission(String name, double lat, double lon, double duration, double temp) {
        super(name, lat, lon, duration, temp); // Call the constructor of the parent class
    }

    @Override
    public void performMission() {
        System.out.println("Supply mission started!");
    }
}
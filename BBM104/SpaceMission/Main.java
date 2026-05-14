import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {

        //Get variables from input file, spacecraft name, and total energy from command-line arguments
        String inputFile = args[0];
        String spacecraftName = args[1];
        double totalEnergy = Double.parseDouble(args[2]);

        // Wrap the reading part in a try-with-resources block
        try (BufferedReader br = new BufferedReader(new FileReader(inputFile))) {
            String line;
            List<SpacecraftSystem> systems = new ArrayList<>();
            Mission mission = null;

            while ((line = br.readLine()) != null) {
                String[] parts = line.split(",");

                //Switch based on the first part of the line to determine the type of system or mission
                switch (parts[0]) {
                    case "propulSys":
                        //If the line describes a propulsion system, parse and create a PropulsionSystem object
                        if (parts.length == 4) {
                            systems.add(new PropulsionSystem(
                                    Double.parseDouble(parts[1]),
                                    Double.parseDouble(parts[2]),
                                    Double.parseDouble(parts[3])
                            ));
                        }
                        break;

                    case "supportSys":
                        // If the line describes a life support system, parse and create a LifeSupportSystem object
                        if (parts.length == 5) {
                            systems.add(new LifeSupportSystem(
                                    Double.parseDouble(parts[1]), // energy
                                    Double.parseDouble(parts[3]), // oxygen level
                                    Double.parseDouble(parts[2]), // temperature
                                    Double.parseDouble(parts[4])  // multiplier
                            ));
                        }
                        break;

                    case "navSys":
                        // If the line describes a navigation system, parse and create a NavigationSystem object
                        if (parts.length == 4) {
                            systems.add(new NavigationSystem(
                                    Double.parseDouble(parts[1]),
                                    Double.parseDouble(parts[2]),
                                    Double.parseDouble(parts[3])
                            ));
                        }
                        break;

                    case "exploreMission":
                        // If the line describes an exploration mission, parse and create an ExploreMission object
                        if (parts.length == 5) {
                            mission = new ExploreMission(
                                    "Explore Mission",
                                    Double.parseDouble(parts[1]),
                                    Double.parseDouble(parts[2]),
                                    Double.parseDouble(parts[3]),
                                    Double.parseDouble(parts[4])
                            );
                        }
                        break;

                    case "satelliteMission":
                        // If the line describes a satellite mission, parse and create a SatelliteMission object
                        if (parts.length == 5) {
                            mission = new SatelliteMission(
                                    "Satellite Mission",
                                    Double.parseDouble(parts[1]),
                                    Double.parseDouble(parts[2]),
                                    Double.parseDouble(parts[3]),
                                    Double.parseDouble(parts[4])
                            );
                        }
                        break;

                    case "supplyMission":
                        // If the line describes a supply mission, parse and create a SupplyMission object
                        if (parts.length == 5) {
                            mission = new SupplyMission(
                                    "Supply Mission",
                                    Double.parseDouble(parts[1]),
                                    Double.parseDouble(parts[2]),
                                    Double.parseDouble(parts[3]),
                                    Double.parseDouble(parts[4])
                            );
                        }
                        break;

                    default:
                        break;
                }
            }

            // Creating Spacecraft object
            Spacecraft spacecraft = new Spacecraft(spacecraftName, systems, mission, totalEnergy);
            spacecraft.startMission(); // Start the spacecraft mission

        } catch (IOException | NumberFormatException e) {
            // Catching exceptions without printing
        }
    }
}

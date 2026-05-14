import java.io.BufferedReader;
import java.io.FileReader;
import java.time.LocalDate;
import java.util.*;

//Abstract class representing a generic bank account
abstract class Account {
    protected String accountId; //Unique identifier for the account
    protected double balance; //Current balance of the account
    protected List<Transaction> transactions = new ArrayList<>(); //List of transaction associated with the account

    //Constructor to initialize account with id and balance
    public Account(String accountId, double balance) {
        this.accountId = accountId;
        this.balance = balance;
    }

    //Abstract method to process a transaction
    public abstract void processTransaction(Transaction transaction);

    //Add a transaction to the transaction history (ArrayList)
    public void addTransaction(Transaction transaction) {
        transactions.add(transaction);
    }

    //Getter for account id
    public String getAccountId() {
        return accountId;
    }

    //Getter for account balance
    public double getBalance() {
        return balance;
    }

    //Setter for account balance
    public void setBalance(double balance) {
        this.balance = balance;
    }

    //Getter for the list of transaction
    public List<Transaction> getTransactions() {
        return transactions;
    }

    //Abstract method to evaluate the risk of the account
    public abstract void riskEvaluation();

    //Display account information
    public abstract void showInfo();
}

//Cuurent account class
class CurrentAccount extends Account {

    //Max overdraft limit for the account
    private double overdraftLimit;

    //Constructor to initialize account id, balance and overdraft
    public CurrentAccount(String accountId, double balance, double overdraftLimit) {
        super(accountId, balance);
        this.overdraftLimit = overdraftLimit;
    }

    //Processes a transaction for the current account
    @Override
    public void processTransaction(Transaction transaction) {
        double amount = transaction.getAmount();
        if (amount > (balance + overdraftLimit)) {  //Check if transaction exceeds overdraft limit
            System.out.println("Current Account: Amount exceeds overdraft limit. Amount: " + amount + " Balance: " + balance + " Limit: " + overdraftLimit);
            return;
        }
        balance -= amount; //Deduct the transaction amount from balance
        addTransaction(transaction); //Add to the arraylist
    }

    //Evaluate the risk of the current account based on overdraft usage.
    @Override
    public void riskEvaluation() {
        if (balance < 0) { //Account is in overdraft
            double overdraftUsage = Math.abs(balance);
            if (overdraftUsage > overdraftLimit * 0.8) {
                System.out.println("Current Account-Medium Risk: Account is in overdraft.");
            } else {
                System.out.println("Current Account-Low Risk: Account is in stable.");
            }
        }
    }

    @Override
    public void showInfo() {
        System.out.println("Current Account - Account Number: " + accountId);
        System.out.println("Balance: $" + balance);
        System.out.println("Overdraft Limit: $" + overdraftLimit);
    }
}

//Savings account class
class SavingAccount extends Account {
    private double interestRate;
    private double minBalance;

    //Constructor to initialize account id, balance, interest rate and minimum balance
    public SavingAccount(String accountId, double balance, double interestRate, double minBalance) {
        super(accountId, balance);
        this.interestRate = interestRate;
        this.minBalance = minBalance;
    }

    //Processes a transaction for the savings account
    @Override
    public void processTransaction(Transaction transaction) {
        double amount = transaction.getAmount();
        if (amount > (balance + minBalance)) { //Check if withdrawal exceeds permissible amount
            System.out.println("Savings Account: Withdrawal exceeds balance and minimum balance.");
            return;
        }
        if (balance - amount < minBalance) { //Apply penalty if balance falls below min
            double penalty = (minBalance - (balance - amount)) * 0.05;
            balance -= (amount + penalty);
            addTransaction(transaction);
        } else {
            balance -= amount; //Deduct transaction amount normally
            addTransaction(transaction);
        }
    }

    //Evaluates the risk of the savings account based on balance threshold
    @Override
    public void riskEvaluation() {
        if (balance < minBalance * 1.2) {
            System.out.println("Saving Account-High Risk: Balance below required threshold.");
        } else {
            System.out.println("Saving Account-Low Risk: Account is in stable.");
        }
    }

    @Override
    public void showInfo() {
        System.out.println("Savings Account - Account Number: " + accountId);
        System.out.println("Balance: $" + balance);
        System.out.println("Interest Rate: " + interestRate * 100 + "%");
    }
}

//Fixed deposit account class
class FixedDepositAccount extends Account {
    private double interestRate;
    private LocalDate maturityDate;
    private double penaltyRate;

    //Constructor to initialize account id, balance, interest rate, maturity date and penalty rate
    public FixedDepositAccount(String accountId, double balance, double interestRate, LocalDate maturityDate, double penaltyRate) {
        super(accountId, balance);
        this.interestRate = interestRate;
        this.maturityDate = maturityDate;
        this.penaltyRate = penaltyRate;
    }

    //Processes a transaction for the fixed deposit account
    @Override
    public void processTransaction(Transaction transaction) {
        LocalDate currentDate = LocalDate.now();
        if (currentDate.isBefore(maturityDate)) { //Check if the account is mature
            System.out.println("Fixed Deposit Account: Account is not mature.");
            return;
        }
        if (balance < transaction.getAmount()) { //Check for sufficient funds
            System.out.println("Fixed Deposit Account: Insufficient funds.");
            return;
        }
        balance -= transaction.getAmount(); //Deduct transaction amount
        addTransaction(transaction);
    }

    //Evaluate the risk of the fixed deposit account based on maturity date
    @Override
    public void riskEvaluation() {
        LocalDate currentDate = LocalDate.now();
        if (currentDate.isAfter(maturityDate)) {
            System.out.println("Fixed Deposit Account-High Risk: Account is close to maturity date.");
        } else {
            System.out.println("Fixed Deposit Account-Low Risk: Account is stable.");
        }
    }

    @Override
    public void showInfo() {
        System.out.println("Fixed Deposit Account - Account Number: " + accountId);
        System.out.println("Balance: $" + balance);
        System.out.println("Interest Rate: " + interestRate * 100 + "%");
        System.out.println("Maturity Date: " + maturityDate);
        System.out.println("Status: " + (LocalDate.now().isBefore(maturityDate) ? "Active" : "Matured"));
    }
}

//Class representing a transaction between accounts
class Transaction {
    private UUID id;
    private String senderId;
    private String receiverId;
    private double amount;

    //Constructor to initialize sender id, transaction amount and receiver id
    public Transaction(String senderId, double amount, String receiverId) {
        this.id = UUID.randomUUID();
        this.senderId = senderId;
        this.amount = amount;
        this.receiverId = receiverId;
    }

    //Getter for transaction id
    public UUID getId() {
        return id;
    }

    //Getter for transaction amount
    public double getAmount() {
        return amount;
    }

    //Getter for sender id
    public String getSenderId() {
        return senderId;
    }

    //Getter for receiver id
    public String getReceiverId() {
        return receiverId;
    }
}

//Main class for banking system
public class BankingSystem {
    private static Map<String, Account> accounts = new HashMap<>(); //Stores accounts id's
    private static List<Transaction> transactions = new ArrayList<>(); //Stores all transactions

    public static void main(String[] args) throws Exception {
        String accountsFile = args[0];
        String transactionsFile = args[1];

        //Read accounts and transactions from text files
        readAccounts(accountsFile);
        processTransactions(transactionsFile);

        //After processing, display account information and transactions
        for (Account account : accounts.values()) {
            System.out.println("\n****************** Summary for Account " + account.getAccountId() + " ******************");
            account.showInfo();
            account.riskEvaluation();
            for (Transaction transaction : account.getTransactions()) {
                System.out.println("------------------------------------");
                System.out.println("Transaction ID: " + transaction.getId());
                System.out.println("Sender: " + transaction.getSenderId());
                System.out.println("Receiver: " + transaction.getReceiverId());
                System.out.println("Amount: " + transaction.getAmount());
            }
            System.out.println("************************************************************************************************************");
        }
    }

    //Read account details from a file and initializes account objects
    private static void readAccounts(String accountsFile) throws Exception {
        BufferedReader reader = new BufferedReader(new FileReader(accountsFile));
        String line;
        while ((line = reader.readLine()) != null) {
            String[] fields = line.split(",");
            String accountId = fields[0];
            String accountType = fields[1];
            double balance = Double.parseDouble(fields[2]);

            //Check the account type and initialize the appropriate account object
            if (accountType.equals("Current")) {
                //For Current, the fourth field is the overdraft limit
                double overdraftLimit = Double.parseDouble(fields[3]);
                accounts.put(accountId, new CurrentAccount(accountId, balance, overdraftLimit));
            } else if (accountType.equals("Saving")) {
                //For Saving, the fourth field is the interest rate and the fifth field is the minimum balance
                double interestRate = Double.parseDouble(fields[3]);
                double minBalance = Double.parseDouble(fields[4]);
                accounts.put(accountId, new SavingAccount(accountId, balance, interestRate, minBalance));
            } else if (accountType.equals("Deposit")) {
                //For Fixed deposit fourth field is interest rate, fifth field is term in month,
                //sixth field is penalty and seventh field is start date
                double interestRate = Double.parseDouble(fields[3]);
                int termInMonths = Integer.parseInt(fields[4]);
                double penalty = Double.parseDouble(fields[5]);
                LocalDate startDate = LocalDate.parse(fields[6]);
                accounts.put(accountId, new FixedDepositAccount(accountId, balance, interestRate, startDate.plusMonths(termInMonths), penalty));
            }
        }
        reader.close();
    }

    //Read transaction details from a file and processes them for the respective accounts
    private static void processTransactions(String transactionsFile) throws Exception {
        BufferedReader reader = new BufferedReader(new FileReader(transactionsFile));
        String line;
        while ((line = reader.readLine()) != null) {
            String[] fields = line.split(",");
            String senderId = fields[0];
            double amount = Double.parseDouble(fields[1]);
            String receiverId = fields[2];

            //Create a new Transaction object using the parsed data
            Transaction transaction = new Transaction(senderId, amount, receiverId);
            transactions.add(transaction);

            //Retrieve the sender and receiver accounts from the accounts map.
            Account sender = accounts.get(senderId);
            Account receiver = accounts.get(receiverId);

            //Process the transaction for the sender's account
            if (sender != null) {
                sender.processTransaction(transaction);
            }

            //Add the transaction to the receiver's account history (if applicable)
            if (receiver != null) {
                receiver.addTransaction(transaction);
            }
        }
        reader.close();
    }
}

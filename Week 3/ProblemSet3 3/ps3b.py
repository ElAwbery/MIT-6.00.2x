# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

# PROBLEM 1

class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb 

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        
        # clearance decision is randomly determined
        clearance_decision = random.random()
        
        # the ratio of decisions to clear against not to clear represents the probability of clearance 
        # assigned to this virus instance in its attribbute .ClearProb
        if clearance_decision <= self.clearProb:
            return True
        
        return False
       
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        # reproduction decision is randomly determined
        reproduction_outcome = random.random()
        
        if reproduction_outcome <= self.maxBirthProb * (1 - popDensity):
           offspring = SimpleVirus(self.maxBirthProb, self.clearProb)
           
           return offspring
           
        else:
            raise NoChildException
             
SimpleSimon = SimpleVirus(0.8, 0.2)       


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses

    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        return len(self.viruses)       

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
       
        clone_viruses = self.viruses.copy()
        
        for virus in clone_viruses:
            
            if virus.doesClear():
                self.viruses.remove(virus)
        
        popDensity = self.getTotalPop()/self.maxPop
        
        remaining = self.viruses.copy()
        
        for virus in remaining:
            
            try: 
                self.viruses.append(virus.reproduce(popDensity))
                
            except NoChildException:
                pass
                
                
        return self.getTotalPop()
            
      
# PROBLEM 2

def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    # store numbers of particles, each list item is the sum of the particles across all trials
    # so far at that time_step
    # the mean is calculated at the end of the simulation
    
    virus_population_growth = []
    for i in range(300):
        virus_population_growth.append(0)
       
    for trial in range(numTrials):
        #each trial instantiates a patient with numViruses SimpleVirus instances
        patient = Patient([SimpleVirus(maxBirthProb, clearProb) for virus in range(numViruses)], maxPop)
        
        # simulate a single trial
        for time_step in range(300):
            virus_population_growth[time_step] += patient.update()
        
    # the mean virus count of num_trials trials for each of 300 time_steps
    mean_virus_counts = [total/numTrials for total in virus_population_growth]
    
    pylab.plot(mean_virus_counts, label = "SimpleVirus")
    pylab.title("SimpleVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc = "best")
    pylab.show()

# tests

simulationWithoutDrug(1, 1000, 1.0, 0.0, 30)
simulationWithoutDrug(1, 10000, 1.0, 0.0, 30)
'''
# simulationWithoutDrug(100, 1000, 0.1, 0.05, 1)

'''
simulationWithoutDrug(3, 1000, 0.0, 1.0, 30)
simulationWithoutDrug(3, 1000, 0.5, 0.5, 30)
simulationWithoutDrug(3, 1000, 0.3, 0.7, 30)
simulationWithoutDrug(3, 1000, 0.7, 0.3, 100)

simulationWithoutDrug(1, 10, 1.0, 0.0, 1)
simulationWithoutDrug(100, 200, 0.2, 0.8, 1)
simulationWithoutDrug(1, 90, 0.8, 0.1, 1)


# PROBLEM 3

class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb
                  
    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        # if the drug is in the resistances dictionary, it has a boolean value 
        try:
            return self.resistances[drug]
        # if the drug is not in the resistances dictionary
        except:
            return False
        
    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        resistant_to_all = True
        
        for drug in activeDrugs:
            try:
                if self.resistances[drug] == False:
                    resistant_to_all = False
            
            except KeyError:
                resistant_to_all = False
        
        if resistant_to_all:
        
            reproduction_outcome = random.random()
         
            if reproduction_outcome <= self.maxBirthProb * (1 - popDensity):
               
                # Here the resistances are updated to those inherited by the offspring
                # For every drug in self.resistances, the offspring must either inherit (keep True value) 
                # or switch (to False) the resistance value for that drug 
                # The outcome inherit or switch is randomly assigned
                  
                for drug in self.resistances:
                    # a drug eiher inherits or does not inherit the resistance trait
                    inheritance_outcome = random.random()
                    
                    #switch:
                    if inheritance_outcome <= self.mutProb:
                        if self.resistances[drug] == True:
                            self.resistances[drug] = False
                        else:
                            self.resistances[drug] = True
                            
                offspring = ResistantVirus(self.maxBirthProb, self.clearProb, self.resistances, self.mutProb)
                return offspring
            else:
                raise NoChildException
       
        else:
            raise NoChildException
                                          
# tests
            
# create a resistances dict
resistances_test = {'goop':True, 'yuck':True, 'oogy':True, 'gnasty': True}

# create an activedrugs list
drugs = ['goop', 'yuck', 'oogy', 'gnasty']

# create a resistantVirus
Reggie = ResistantVirus(0.7, 0.3, resistances_test, 0.6)
# reproduce tests - boundary entries

virus1 = ResistantVirus(1.0, 0.0, {}, 0.0)
virus1.reproduce(2.0, drugs)

virus3 = ResistantVirus(1.0, 1.0, {}, 0.0)
virus3.reproduce(2.0, drugs)

virus4 = ResistantVirus(1.0, 0.0, {'drug1':True, 'drug2': True, 'drug3': True, 'drug4': True, 'drug5': True, 'drug6': True}, 0.5)          
virus4.reproduce(0, [])

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        Patient.__init__(self, viruses, maxPop)
        self.prescriptions = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.prescriptions:
            self.prescriptions.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.prescriptions

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        resistant_virus_total = 0
        for virus in self.viruses:
            
            if type(virus) is ResistantVirus:
                resistant_to_all = True
              
                for drug in drugResist:
                    known_resistances = virus.getResistances()
                    
                    if drug not in known_resistances:
                        resistant_to_all = False
                      
                    elif known_resistances[drug] == False:
                        resistant_to_all = False
                    # executes only if no known non-resistance to any of the drugs in druglist
                    # and all drugs in list are entered in the virus' resistances dict (no key errors raised)
                    
                if resistant_to_all: 
                    resistant_virus_total += 1
    
        return resistant_virus_total

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        
        #update for non-treated patient:
      
        clone_viruses = self.viruses.copy()
        
        for virus in clone_viruses:
            
            if virus.doesClear():
                self.viruses.remove(virus)
        
        popDensity = self.getTotalPop()/self.maxPop
        
        remaining = self.viruses.copy()
        
        for virus in remaining:
            
            if type(virus) == ResistantVirus:
                
                try:
                    offspring = virus.reproduce(popDensity, self.prescriptions)
                except NoChildException:
                    pass
                else:
                    if offspring == None:
                        print("EEEVIL")
                    self.viruses.append(offspring)
         
            elif type(virus) == SimpleVirus:
                
                offspring = virus.reproduce(popDensity, self.prescriptions)
                if offspring == None:
                    pass
                
                else:
                    self.viruses.append(offspring)

        return self.getTotalPop()
            
virus1 = ResistantVirus(1.0, 0.0, {"drug1": True}, 0.0)
virus2 = ResistantVirus(1.0, 0.0, {"drug1": False}, 0.0)
patient = TreatedPatient([virus1, virus2], 1000000)
patient.addPrescription("drug1")

# Updating patient 5 times
# Expect resistant population to be 2^5 +/- 10
# Expect total population to be the resistant population plus 1
# now passed

womby_recovering = TreatedPatient([SimpleSimon, virus1, virus3], 200)
womby_recovering.addPrescription('goop')
womby_recovering.addPrescription('oogy')
womby_recovering.addPrescription('drug1')
womby_recovering.addPrescription('drug2')
womby_recovering.addPrescription('drug3')
womby_recovering.addPrescription('drug4')
womby_recovering.addPrescription('drug5')
womby_recovering.addPrescription('drug6')
wr_druglist = womby_recovering.getPrescriptions()
womby_recovering.getResistPop(wr_druglist)

womby_recovering.update()


virus1 = ResistantVirus(1.0, 0.0, {"drug1": True}, 0.0)
virus2 = ResistantVirus(1.0, 0.0, {"drug1": False, "drug2": True}, 0.0)
virus3 = ResistantVirus(1.0, 0.0, {"drug1": True, "drug2": True}, 0.0)
patient = TreatedPatient([virus1, virus2, virus3], 100)
patient.getResistPop(['drug1']) # 2
patient.getResistPop(['drug2']) # 2


patient.getResistPop(['drug1','drug2']) # expected 1, got 3
patient.getResistPop(['drug3']) # 0
patient.getResistPop(['drug1', 'drug3']) # expected 0, got 3
patient.getResistPop(['drug1','drug2', 'drug3']) # expected 0, got 3

# PROBLEM 4

# create a treated patient with 100 resistant virus instances and maximum sustainable population 1000
# A few good questions to consider as you look at your plots are: 
# What trends do you observe? Are the trends consistent with your intuition? 

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    virus_totals = []
    guttagonol_resistant_viruses = []
    
    # adds a base count of 0 viruses for each timestep
    for i in range(300):
        virus_totals.append(0)
        guttagonol_resistant_viruses.append(0)
    
    for trial in range(numTrials):
        # each trial instantiates a patient with 100 viruses
        tp_viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for num in range(numViruses)]
        patient = TreatedPatient(tp_viruses, maxPop)
        
        for time_step in range(150):
            # each update returns total virus population
            virus_totals[time_step] += patient.update()
            guttagonol_resistant_viruses[time_step] += patient.getResistPop(['guttagonol'])
        
        patient.addPrescription('guttagonol')
        
        for time_step in range(150, 300):
            virus_totals[time_step] += patient.update()
            guttagonol_resistant_viruses[time_step] += patient.getResistPop(['guttagonol'])
            
    # the mean virus count of num_trials trials for each of 300 time_steps
    mean_total_virus_counts = [total/numTrials for total in virus_totals]
    mean_guttagonol_resistant_viruses = [total/numTrials for total in guttagonol_resistant_viruses]
    
    #print("viruses:", virus_totals)
    #print("g-resistant", guttagonol_resistant_viruses)
    
    pylab.plot(mean_total_virus_counts, color = 'b', label = "All Viruses")
    pylab.plot(mean_guttagonol_resistant_viruses, color = 'r', label = "Guttagonol resistant")
    pylab.title("Treated Patient simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Populations")
    pylab.legend(loc = "upper right")
    pylab.show()
    
# prescribed test
simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5)
simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5)
simulationWithDrug(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.05, 50)
simulationWithDrug(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.05, 75)
simulationWithDrug(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.05, 100)

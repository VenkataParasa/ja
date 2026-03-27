import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, ActivityIndicator, TouchableOpacity, Alert, Image, Modal, TextInput } from 'react-native';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

const App = () => {
  const [businesses, setBusinesses] = useState([]);
  const [students, setStudents] = useState([]);
  const [bankAccounts, setBankAccounts] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [showStudentLoginForm, setShowStudentLoginForm] = useState(false);
  const [studentLoginNumber, setStudentLoginNumber] = useState('');
  const [studentLoginLastName, setStudentLoginLastName] = useState('');
  const [roles, setRoles] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [currentView, setCurrentView] = useState('dashboard');
  const [selectedBusinessId, setSelectedBusinessId] = useState(null);
  const [simulationStatus, setSimulationStatus] = useState('Active'); // Active, Paused, Completed
  const [activeIncident, setActiveIncident] = useState('None');
  const [incidentMessage, setIncidentMessage] = useState('');
  const [businessXP, setBusinessXP] = useState({});
  const [businessContributions, setBusinessContributions] = useState({});
  const [donationAmount, setDonationAmount] = useState('50');
  const [posAmount, setPosAmount] = useState('');
  const [posItemName, setPosItemName] = useState('General Merchandise');
  const [manualTransferAmount, setManualTransferAmount] = useState('');
  const [selectedIncidentType, setSelectedIncidentType] = useState('Tornado');
  const [customIncidentMessage, setCustomIncidentMessage] = useState('');

  const roleTaskMap = {
    CEO: ['Approve Loan', 'Review sales performance', 'Authorize high-priority expenses'],
    CFO: ['Pay Bills', 'Review account balances', 'Prepare end-of-day finance summary'],
    Accountant: ['Pay Bills', 'Reconcile transactions', 'Support payroll processing'],
    Employee: ['Process Sales', 'Assist customers', 'Restock and organize inventory']
  };

  useEffect(() => {
    fetchAllData();
  }, [isLoggedIn]);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      const [businessesRes, studentsRes, accountsRes, transactionsRes, rolesRes, simulationRes, leaderboardRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/businesses`),
        axios.get(`${API_BASE_URL}/students`),
        axios.get(`${API_BASE_URL}/bankaccounts`),
        axios.get(`${API_BASE_URL}/transactions`),
        axios.get(`${API_BASE_URL}/roles`),
        axios.get(`${API_BASE_URL}/simulation`),
        axios.get(`${API_BASE_URL}/leaderboard`)
      ]);
      
      setBusinesses(businessesRes.data);
      setStudents(studentsRes.data);
      setBankAccounts(accountsRes.data);
      setTransactions(transactionsRes.data);
      setRoles(rolesRes.data);
      setLeaderboard(leaderboardRes.data);
      
      // Update persistent simulation state
      if (simulationRes.data) {
        setSimulationStatus(simulationRes.data.status);
        setActiveIncident(simulationRes.data.activeIncident || 'None');
        setIncidentMessage(simulationRes.data.incidentMessage || '');
        try {
          setBusinessXP(JSON.parse(simulationRes.data.xpData || '{}'));
          setBusinessContributions(JSON.parse(simulationRes.data.contributionData || '{}'));
        } catch (e) {
          console.error('Error parsing simulation data:', e);
        }
      }
      
      setError(null);
    } catch (err) {
      const errorMsg = `Failed to fetch data: ${err.message}${err.response ? ` (${err.response.status} ${err.response.statusText})` : ''}`;
      setError(errorMsg);
      console.error('Error fetching data:', err);
      if (err.response) {
        console.error('Response data:', err.response.data);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = (role, student = null) => {
    if (student) {
      setCurrentUser({
        id: student.studentId,
        name: `${student.firstName} ${student.lastName}`,
        role: 'student',
        businessId: student.businessId,
        jobTitle: roles.find(r => r.roleId === student.roleId)?.roleName || 'Student'
      });
    } else {
      setCurrentUser({
        id: role === 'teacher' ? 201 : 301,
        name: role.charAt(0).toUpperCase() + role.slice(1) + ' Account',
        role: role,
        businessId: null
      });
    }
    
    setIsLoggedIn(true);
    setShowStudentLoginForm(false);
  };

  const handleStudentLoginSubmit = () => {
    const enteredNumber = studentLoginNumber.trim().toUpperCase();
    const enteredLastName = studentLoginLastName.trim().toLowerCase();

    if (!enteredNumber || !enteredLastName) {
      alert('Please enter your Student Number and Last Name.');
      return;
    }

    const matchedStudent = students.find((student) => {
      const numberMatch = (student.studentNumber || '').trim().toUpperCase() === enteredNumber;
      const lastNameMatch = (student.lastName || '').trim().toLowerCase() === enteredLastName;
      return numberMatch && lastNameMatch;
    });

    if (!matchedStudent) {
      alert('Student not found. Check your Student Number and Last Name.');
      return;
    }

    handleLogin('student', matchedStudent);
    setStudentLoginNumber('');
    setStudentLoginLastName('');
  };
  
  const handleIncidentDecision = async (decision) => {
    const businessId = currentUser?.businessId;
    if (!businessId) return;

    let newXPMap = { ...businessXP };
    let newContributionMap = { ...businessContributions };

    if (decision === 'contribute') {
      const business = businesses.find(b => b.businessId === businessId);
      if (business && business.currentBalance >= 50) {
        newContributionMap[businessId] = 'contributed';
        newXPMap[businessId] = (newXPMap[businessId] || 0) + 500;
        
        // Update frontend balance for immediate feedback
        setBusinesses(prev => prev.map(b => 
          b.businessId === businessId ? { ...b, currentBalance: b.currentBalance - 50 } : b
        ));
      } else {
        alert('Your business does not have enough funds to afford this. Please check your dashboard.');
        return;
      }
    } else {
      newContributionMap[businessId] = 'declined';
      newXPMap[businessId] = (newXPMap[businessId] || 0) - 200;
    }

    // Persist to backend
    try {
      setBusinessXP(newXPMap);
      setBusinessContributions(newContributionMap);
      await axios.post(`${API_BASE_URL}/simulation/update-data`, {
        xpData: JSON.stringify(newXPMap),
        contributionData: JSON.stringify(newContributionMap)
      });
    } catch (err) {
      console.error('Error saving decision:', err);
    }
  };

  const handleLogout = () => {
    if (window.confirm('Are you sure you want to logout?')) {
      setIsLoggedIn(false);
      setCurrentUser(null);
      setShowStudentLoginForm(false);
      setStudentLoginNumber('');
      setStudentLoginLastName('');
      setCurrentView('dashboard');
      setError(null);
      setSelectedBusinessId(null);
    }
  };

  const handleDepositPaycheck = async () => {
    try {
      const studentObj = students.find(s => s.studentId === currentUser.id);
      const roleObj = roles.find(r => r.roleId === studentObj?.roleId);
      const amount = roleObj?.baseSalary || 100;

      const response = await axios.post(`${API_BASE_URL}/bank/deposit-paycheck`, {
        studentId: currentUser.id,
        amount: amount
      });

      const updatedAccountId = response?.data?.accountId;
      const updatedBalance = response?.data?.newBalance;
      if (updatedAccountId && typeof updatedBalance === 'number') {
        setBankAccounts(prev => {
          const existingIndex = prev.findIndex(a => a.accountId === updatedAccountId);
          if (existingIndex >= 0) {
            return prev.map(a => a.accountId === updatedAccountId ? { ...a, balance: updatedBalance } : a);
          }
          return [
            ...prev,
            {
              accountId: updatedAccountId,
              balance: updatedBalance,
              accountType: 'Personal',
              accountHolderName: `${studentObj?.firstName || ''} ${studentObj?.lastName || ''}`.trim(),
              students: [{ studentId: currentUser.id }]
            }
          ];
        });
      }

      alert(`Success! Successfully deposited $${amount} into your personal account.`);
      await fetchAllData();
    } catch (err) {
      alert(err.response?.data || 'Failed to deposit paycheck. Check your personal account.');
    }
  };

  const handleApplyLoan = async () => {
    const amountStr = prompt('Enter the loan amount requested for your business:');
    if (!amountStr) return;
    const amount = parseFloat(amountStr);
    if (isNaN(amount) || amount <= 0) return;

    try {
      await axios.post(`${API_BASE_URL}/bank/apply-loan`, {
        businessId: currentUser.businessId,
        amount: amount,
        studentId: currentUser.id
      });
      alert(`Loan of $${amount} approved for your business!`);
      fetchAllData();
    } catch (err) {
      alert(err.response?.data || 'Failed to apply for loan.');
    }
  };

  const handleDonate = async () => {
    const amount = parseFloat(donationAmount);
    if (isNaN(amount) || amount <= 0) return;

    try {
      await axios.post(`${API_BASE_URL}/bank/donate`, {
        businessId: currentUser.businessId,
        amount: amount
      });
      alert(`Thank you for your $${amount} donation! Your Civic Score has increased.`);
      setDonationAmount('50');
      fetchAllData();
    } catch (err) {
      alert(err.response?.data || 'Failed to process donation.');
    }
  };

  const handlePosSale = async () => {
    const amount = parseFloat(posAmount);
    if (isNaN(amount) || amount <= 0) {
      alert('Please enter a valid amount.');
      return;
    }

    try {
      await axios.post(`${API_BASE_URL}/bank/pos-sale`, {
        businessId: currentUser.businessId,
        amount: amount,
        itemName: posItemName
      });
      alert(`Sale of $${amount} processed successfully! Business balance updated.`);
      setPosAmount('');
      setManualTransferAmount('');
      fetchAllData();
    } catch (err) {
      alert('Failed to process sale.');
    }
  };

  const getStudentRoleName = () => {
    if (!currentUser || currentUser.role !== 'student') return '';
    const studentObj = students.find(s => s.studentId === currentUser.id);
    return (roles.find(r => r.roleId === studentObj?.roleId)?.roleName || currentUser.jobTitle || 'Employee');
  };

  const isLoanRole = () => {
    const roleName = (getStudentRoleName() || '').toUpperCase();
    return roleName === 'CEO' || roleName === 'CFO' || roleName === 'ACCOUNTANT';
  };

  const getRoleTasks = () => {
    const roleName = getStudentRoleName();
    if (roleTaskMap[roleName]) return roleTaskMap[roleName];
    if (roleName === 'Manager') return roleTaskMap.CEO;
    return roleTaskMap.Employee;
  };

  const getCurrentStudent = () => {
    if (!currentUser || currentUser.role !== 'student') return null;
    return students.find(s => s.studentId === currentUser.id) || null;
  };

  const getPersonalWalletBalance = () => {
    const studentObj = getCurrentStudent();
    if (!studentObj) return 0;

    const byLinkedAccount = studentObj.bankAccountId
      ? bankAccounts.find(a => a.accountId === studentObj.bankAccountId)
      : null;
    if (byLinkedAccount) return byLinkedAccount.balance || 0;

    const byStudentsArray = bankAccounts.find(
      a => a.accountType === 'Personal' && Array.isArray(a.students) && a.students.some(s => s.studentId === studentObj.studentId)
    );
    if (byStudentsArray) return byStudentsArray.balance || 0;

    const byAccountHolder = bankAccounts.find(
      a => a.accountType === 'Personal' && (a.accountHolderName || '').toLowerCase() === `${studentObj.firstName} ${studentObj.lastName}`.toLowerCase()
    );
    return byAccountHolder?.balance || 0;
  };

  const getCurrentBusinessBalance = () => {
    if (!currentUser?.businessId) return 0;
    return businesses.find(b => b.businessId === currentUser.businessId)?.currentBalance || 0;
  };

  const getIncidentDefaultMessage = (incidentType) => {
    switch (incidentType) {
      case 'Tornado':
        return 'A Tornado has struck the park! Decide how to respond.';
      case 'Power Outage':
        return 'Town blackout! Invest $200 in backup generators to prevent inventory spoilage?';
      case 'News Flash':
        return "Mayor's Visit! Clean facilities and pay a $50 sponsorship fee?";
      default:
        return '';
    }
  };

  const broadcastIncident = async () => {
    const incidentType = selectedIncidentType || 'None';
    const message = customIncidentMessage.trim() || getIncidentDefaultMessage(incidentType);
    try {
      const res = await axios.post(`${API_BASE_URL}/simulation/trigger-incident`, {
        incidentType,
        incidentMessage: message
      });
      if (res.data) {
        setActiveIncident(res.data.activeIncident);
        setIncidentMessage(res.data.incidentMessage);
        setBusinessContributions(JSON.parse(res.data.contributionData || '{}'));
      }
    } catch (err) {
      console.error(err);
      alert('Failed to broadcast incident');
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const renderLogin = () => (
    <View style={styles.container}>
      <View style={styles.loginContainer}>
        {/* Background Pattern */}
        <View style={styles.loginBackground}>
          <View style={styles.loginOverlay} />
        </View>
        
        {/* Login Content */}
        <ScrollView contentContainerStyle={styles.loginScrollContent} style={styles.loginContent}>
          {/* Logo Section */}
          <View style={styles.logoSection}>
            <View style={styles.logoCircle}>
              <Text style={styles.logoText}>JA</Text>
            </View>
            <Text style={styles.logoSubtitle}>Junior Achievement</Text>
            <Text style={styles.logoDescription}>Education For What's Next™</Text>
          </View>
          
          {/* Welcome Section */}
          <View style={styles.welcomeSection}>
            <Text style={styles.welcomeTitle}>Welcome to JA BizTown</Text>
            <Text style={styles.welcomeDescription}>
              Experience the premier economic simulation that prepares young people for success in a global economy. 
              Choose your role to begin your journey.
            </Text>
          </View>
                    {/* Role Selection or Student Login */}
          <View style={styles.roleSection}>
            {showStudentLoginForm ? (
              <>
                <Text style={styles.roleSectionTitle}>Student Sign In</Text>
                <View style={styles.studentLoginCard}>
                  <Text style={styles.loginFieldLabel}>Student Number</Text>
                  <TextInput
                    style={styles.loginFieldInput}
                    value={studentLoginNumber}
                    onChangeText={setStudentLoginNumber}
                    autoCapitalize="characters"
                    placeholder="Example: STU001"
                  />
                  <Text style={styles.loginFieldLabel}>Last Name</Text>
                  <TextInput
                    style={styles.loginFieldInput}
                    value={studentLoginLastName}
                    onChangeText={setStudentLoginLastName}
                    autoCapitalize="words"
                    placeholder="Enter your last name"
                  />
                  <TouchableOpacity
                    style={styles.studentLoginButton}
                    onPress={handleStudentLoginSubmit}
                  >
                    <Text style={styles.actionButtonText}>Sign In</Text>
                  </TouchableOpacity>
                </View>
                <TouchableOpacity 
                  style={{ marginTop: 16, padding: 12, alignItems: 'center' }} 
                  onPress={() => setShowStudentLoginForm(false)}
                >
                  <Text style={{ color: '#00A0AF', fontWeight: '700' }}>← Back to Roles</Text>
                </TouchableOpacity>
              </>
            ) : (
              <>
                <Text style={styles.roleSectionTitle}>Choose Your Role</Text>
                
                <TouchableOpacity style={[styles.roleCard, styles.studentRole]} onPress={() => setShowStudentLoginForm(true)}>
                  <View style={styles.roleIcon}>
                    <Text style={styles.roleIconText}>👤</Text>
                  </View>
                  <View style={styles.roleInfo}>
                    <Text style={styles.roleTitle}>Student Login</Text>
                    <Text style={styles.roleDescription}>Access your personal dashboard and manage your business tasks.</Text>
                  </View>
                </TouchableOpacity>

                <TouchableOpacity style={[styles.roleCard, styles.teacherRole]} onPress={() => handleLogin('teacher')}>
                  <View style={styles.roleIcon}>
                    <Text style={styles.roleIconText}>🎓</Text>
                  </View>
                  <View style={styles.roleInfo}>
                    <Text style={styles.roleTitle}>Educator Portal</Text>
                    <Text style={styles.roleDescription}>Monitor student progress and manage simulation phases.</Text>
                  </View>
                </TouchableOpacity>

                <TouchableOpacity style={[styles.roleCard, styles.adminRole]} onPress={() => handleLogin('admin')}>
                  <View style={styles.roleIcon}>
                    <Text style={styles.roleIconText}>⚙️</Text>
                  </View>
                  <View style={styles.roleInfo}>
                    <Text style={styles.roleTitle}>Administrator</Text>
                    <Text style={styles.roleDescription}>Control town-wide parameters and system settings.</Text>
                  </View>
                </TouchableOpacity>
              </>
            )}
          </View>
          
          {/* Footer */}
          {renderMainFooter()}
        </ScrollView>
      </View>
    </View>
  );

  const renderMainFooter = () => (
    <View style={styles.mainFooter}>
      <View style={styles.footerSection}>
        <Text style={styles.footerTitle}>Get Involved with Junior Achievement!</Text>
        <View style={styles.footerLinks}>
          <TouchableOpacity style={styles.footerLink}>
            <Text style={styles.footerLinkText}>Contact Us</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.footerLink}>
            <Text style={styles.footerLinkText}>Volunteers</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.footerLink}>
            <Text style={styles.footerLinkText}>Educators and Parents</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.footerLink}>
            <Text style={styles.footerLinkText}>Partners</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.footerLink}>
            <Text style={styles.footerLinkText}>About</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.footerLink}>
            <Text style={styles.footerLinkText}>Learning Experiences</Text>
          </TouchableOpacity>
        </View>
      </View>
      <View style={styles.footerBottom}>
        <Text style={styles.footerCopy}>© 2024 Junior Achievement USA. All rights reserved.</Text>
        <Text style={styles.footerMission}>Empowering young people to own their economic success</Text>
      </View>
    </View>
  );

  const renderNavigation = () => (
    <View style={styles.navigationBar}>
      <TouchableOpacity 
        style={[styles.navButton, currentView === 'dashboard' && styles.navButtonActive]}
        onPress={() => setCurrentView('dashboard')}
      >
        <Text style={[styles.navButtonText, currentView === 'dashboard' && styles.navButtonTextActive]}>📊 Dashboard</Text>
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={[styles.navButton, currentView === 'businesses' && styles.navButtonActive]}
        onPress={() => setCurrentView('businesses')}
      >
        <Text style={[styles.navButtonText, currentView === 'businesses' && styles.navButtonTextActive]}>🏢 Businesses</Text>
      </TouchableOpacity>

      <TouchableOpacity 
        style={[styles.navButton, currentView === 'students' && styles.navButtonActive]}
        onPress={() => setCurrentView('students')}
      >
        <Text style={[styles.navButtonText, currentView === 'students' && styles.navButtonTextActive]}>👥 Students</Text>
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={[styles.navButton, currentView === 'accounts' && styles.navButtonActive]}
        onPress={() => setCurrentView('accounts')}
      >
        <Text style={[styles.navButtonText, currentView === 'accounts' && styles.navButtonTextActive]}>💳 Accounts</Text>
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={[styles.navButton, currentView === 'transactions' && styles.navButtonActive]}
        onPress={() => setCurrentView('transactions')}
      >
        <Text style={[styles.navButtonText, currentView === 'transactions' && styles.navButtonTextActive]}>🧾 Transactions</Text>
      </TouchableOpacity>
      
      {currentUser?.role === 'admin' && (
        <TouchableOpacity 
          style={[styles.navButton, currentView === 'leaderboard' && styles.navButtonActive]}
          onPress={() => setCurrentView('leaderboard')}
        >
          <Text style={[styles.navButtonText, currentView === 'leaderboard' && styles.navButtonTextActive]}>🏆 Leaderboard</Text>
        </TouchableOpacity>
      )}
      
      <TouchableOpacity 
        style={[styles.navButton, currentView === 'voting' && styles.navButtonActive]}
        onPress={() => setCurrentView('voting')}
      >
        <Text style={[styles.navButtonText, currentView === 'voting' && styles.navButtonTextActive]}>🗳️ Voting</Text>
      </TouchableOpacity>

      {currentUser?.role === 'student' && (
        <TouchableOpacity 
          style={[styles.navButton, currentView === 'pos' && styles.navButtonActive, { backgroundColor: '#f9f5ff', borderWidth: 1, borderColor: '#cad9de', marginTop: 8 }]}
          onPress={() => setCurrentView('pos')}
        >
          <Text style={[styles.navButtonText, currentView === 'pos' && styles.navButtonTextActive, { color: '#8e44ad' }]}>💵 Point of Sale (POS)</Text>
        </TouchableOpacity>
      )}
      
      <TouchableOpacity style={[styles.logoutButton, { marginTop: 'auto' }]} onPress={handleLogout}>
        <Text style={styles.logoutButtonText}>🚪 Logout</Text>
      </TouchableOpacity>
    </View>
  );

  const renderDashboard = () => (
    <View style={styles.section}>
      <Text style={styles.welcomeText}>Welcome, {currentUser?.name}!</Text>
      <Text style={styles.roleText}>Role: {currentUser?.role}</Text>
      
      {/* Stats Overview */}
      <View style={styles.statsContainer}>
        <TouchableOpacity style={styles.statCard} onPress={() => setCurrentView('businesses')}>
          <Text style={styles.statNumber}>{businesses.length}</Text>
          <Text style={styles.statLabel}>Businesses</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.statCard} onPress={() => setCurrentView('students')}>
          <Text style={styles.statNumber}>{students.length}</Text>
          <Text style={styles.statLabel}>Students</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.statCard} onPress={() => setCurrentView('accounts')}>
          <Text style={styles.statNumber}>{bankAccounts.length}</Text>
          <Text style={styles.statLabel}>Accounts</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.statCard} onPress={() => setCurrentView('transactions')}>
          <Text style={styles.statNumber}>{transactions.length}</Text>
          <Text style={styles.statLabel}>Transactions</Text>
        </TouchableOpacity>
      </View>
      
      {/* Total Balance */}
      {currentUser?.role !== 'student' ? (
        <View style={styles.totalBalanceContainer}>
          <Text style={styles.totalBalanceLabel}>Total System Balance</Text>
          <Text style={styles.totalBalanceAmount}>
            ${bankAccounts.reduce((sum, account) => sum + (account.balance || 0), 0).toLocaleString()}
          </Text>
        </View>
      ) : (
        <View style={styles.totalBalanceContainer}>
          <Text style={styles.totalBalanceLabel}>Your Business Account Balance</Text>
          <Text style={styles.totalBalanceAmount}>
            {formatCurrency(getCurrentBusinessBalance())}
          </Text>
        </View>
      )}

      {/* Student Portal: Wallet & Tasks (RFP Requirement) */}
      {currentUser?.role === 'student' && (
        <>
          <View style={[styles.card, { marginTop: 24, paddingBottom: 24 }]}>
            <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 16 }}>
              <View style={[styles.roleIcon, { marginRight: 12 }]}>
                <Text style={styles.roleIconText}>👤</Text>
              </View>
              <View>
                <Text style={styles.cardTitle}>{getStudentRoleName()} - Job Checklist</Text>
                <Text style={styles.cardDescription}>Complete your required tasks for full simulation XP.</Text>
              </View>
            </View>
            <View style={{ marginTop: 12 }}>
              {getRoleTasks().map((task, idx) => (
                <Text key={`${task}-${idx}`} style={{ marginBottom: 8, fontSize: 16 }}>✅ {task}</Text>
              ))}
              <Text style={{ marginBottom: 16, color: '#00A0AF', fontWeight: 'bold', fontSize: 16 }}>
                🎯 Current Goal: {isLoanRole() ? 'Maintain healthy cash flow' : 'Complete 5 POS transactions'}
              </Text>
              {isLoanRole() ? (
                <TouchableOpacity
                  style={[styles.actionButton, { backgroundColor: '#22404D' }]}
                  onPress={handleApplyLoan}
                >
                  <Text style={styles.actionButtonText}>🏦 Request Business Loan</Text>
                </TouchableOpacity>
              ) : (
                <TouchableOpacity
                  style={[styles.actionButton, { backgroundColor: '#22404D' }]}
                  onPress={() => setCurrentView('pos')}
                >
                  <Text style={styles.actionButtonText}>💵 Process Sales in POS</Text>
                </TouchableOpacity>
              )}
            </View>
          </View>

          <View style={{ flexDirection: 'row', flexWrap: 'wrap', marginTop: 24 }}>
            <View style={[styles.card, { flex: 1, minWidth: 300, marginRight: 16, marginBottom: 16, borderLeftWidth: 6, borderLeftColor: '#00A0AF' }]}>
              <Text style={styles.cardTitle}>Personal Digital Wallet</Text>
              <Text style={styles.cardDescription}>Manage your paycheck and personal funds.</Text>
              <View style={{ flexDirection: 'row', alignItems: 'center', marginTop: 16 }}>
                <Text style={{ fontSize: 32, fontWeight: 'bold', color: '#285F74', marginRight: 24 }}>
                  {formatCurrency(getPersonalWalletBalance())}
                </Text>
                <TouchableOpacity 
                  style={[styles.actionButton, { backgroundColor: '#E3E24F' }]}
                  onPress={handleDepositPaycheck}
                >
                  <Text style={[styles.actionButtonText, { color: '#22404D' }]}>💵 Deposit Paycheck</Text>
                </TouchableOpacity>
              </View>

              <View style={{ marginTop: 18, paddingTop: 14, borderTopWidth: 1, borderTopColor: '#dce9ed' }}>
                <Text style={[styles.cardTitle, { fontSize: 15, marginBottom: 8 }]}>Digital Banking</Text>
                {isLoanRole() && (
                  <TouchableOpacity
                    style={[styles.actionButton, { backgroundColor: '#22404D', marginBottom: 10 }]}
                    onPress={handleApplyLoan}
                  >
                    <Text style={styles.actionButtonText}>🏦 Request Business Loan</Text>
                  </TouchableOpacity>
                )}
                <Text style={{ color: '#285F74', marginBottom: 8 }}>Tap-to-Pay (QR simulation)</Text>
                <View style={{ backgroundColor: '#f4f6f8', borderRadius: 10, borderWidth: 1, borderColor: '#cad9de', padding: 12, marginBottom: 8 }}>
                  <Text style={{ textAlign: 'center', color: '#5a7a87', fontSize: 28 }}>▦</Text>
                  <Text style={{ textAlign: 'center', color: '#5a7a87' }}>QR Placeholder</Text>
                </View>
                <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                  <TextInput
                    style={[styles.input, { flex: 1, marginRight: 8, marginBottom: 0 }]}
                    value={manualTransferAmount}
                    onChangeText={setManualTransferAmount}
                    keyboardType="numeric"
                    placeholder="Manual transfer amount"
                  />
                  <TouchableOpacity
                    style={[styles.actionButton, { backgroundColor: '#00A0AF', minWidth: 110 }]}
                    onPress={() => {
                      setPosAmount(manualTransferAmount);
                      setCurrentView('pos');
                    }}
                  >
                    <Text style={styles.actionButtonText}>Transfer</Text>
                  </TouchableOpacity>
                </View>
              </View>
            </View>

            <View style={[styles.card, { flex: 1, minWidth: 300, marginBottom: 16, backgroundColor: '#f9f5ff', borderColor: '#9b59b6', borderWidth: 1 }]}>
              <Text style={[styles.cardTitle, { color: '#8e44ad' }]}>Civic Virtue: Philanthropy</Text>
              <Text style={styles.cardDescription}>Boost your business's Civic Score by donating to the community.</Text>
              <View style={{ flexDirection: 'row', alignItems: 'center', marginTop: 16 }}>
                <Text style={{ fontSize: 20, color: '#22404D', marginRight: 8 }}>$</Text>
                <TextInput
                  style={[styles.input, { flex: 1, marginRight: 12, marginBottom: 0 }]}
                  value={donationAmount}
                  onChangeText={setDonationAmount}
                  keyboardType="numeric"
                  placeholder="0.00"
                />
                <TouchableOpacity 
                  style={[styles.actionButton, { backgroundColor: '#8e44ad', minWidth: 100 }]}
                  onPress={handleDonate}
                >
                  <Text style={styles.actionButtonText}>💕 Donate</Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
        </>
      )}

      {/* Student Leaderboard Status */}
      {currentUser?.role === 'student' && (
        <View style={[styles.card, { marginTop: 8, backgroundColor: '#f0f9fa', borderColor: '#00A0AF', borderWidth: 1 }]}>
          <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
            <View>
              <Text style={[styles.cardTitle, { color: '#22404D' }]}>Your Business Standing</Text>
              <Text style={{ fontSize: 16, color: '#285F74' }}>
                Ranked <Text style={{ fontWeight: '800', color: '#00A0AF' }}>#{leaderboard.find(e => e.businessId === currentUser.businessId)?.rank || '--'}</Text> in JA BizTown
              </Text>
            </View>
            <Text style={{ fontSize: 40 }}>🏆</Text>
          </View>
          
          <View style={{ marginTop: 16 }}>
            <Text style={{ fontWeight: '700', color: '#22404D', marginBottom: 8 }}>💡 How to increase your rank:</Text>
            {leaderboard.find(e => e.businessId === currentUser.businessId)?.tips.map((tip, idx) => (
              <Text key={idx} style={{ color: '#285F74', marginBottom: 4 }}>• {tip}</Text>
            )) || <Text>Loading success tips...</Text>}
          </View>
        </View>
      )}

      {/* Admin Simulation Controls (RFP Requirement) */}
      {currentUser?.role === 'admin' && (
        <View style={[styles.card, { marginTop: 24, borderLeftWidth: 6, borderLeftColor: '#E3E24F' }]}>
          <Text style={styles.cardTitle}>Simulation Management</Text>
          <Text style={styles.cardDescription}>Current Status: <Text style={{ fontWeight: '800', color: simulationStatus === 'Active' ? '#28a745' : '#dc3545' }}>{simulationStatus}</Text></Text>
          <View style={{ flexDirection: 'row', marginTop: 16, flexWrap: 'wrap' }}>
            <TouchableOpacity 
              style={[styles.actionButton, { backgroundColor: '#00A0AF', marginRight: 12, marginBottom: 8 }]} 
              onPress={async () => {
                setSimulationStatus('Active');
                await axios.post(`${API_BASE_URL}/simulation/status`, "Active", { headers: { 'Content-Type': 'application/json' } });
              }}
            >
              <Text style={styles.actionButtonText}>▶ Start / Resume</Text>
            </TouchableOpacity>
            <TouchableOpacity 
              style={[styles.actionButton, { backgroundColor: '#E3E24F', marginRight: 12, marginBottom: 8 }]} 
              onPress={async () => {
                setSimulationStatus('Paused');
                await axios.post(`${API_BASE_URL}/simulation/status`, "Paused", { headers: { 'Content-Type': 'application/json' } });
              }}
            >
              <Text style={[styles.actionButtonText, { color: '#22404D' }]}>⏸ Pause</Text>
            </TouchableOpacity>
            <TouchableOpacity 
              style={[styles.actionButton, { backgroundColor: '#22404D', marginBottom: 8 }]} 
              onPress={async () => {
                setSimulationStatus('Completed');
                await axios.post(`${API_BASE_URL}/simulation/status`, "Completed", { headers: { 'Content-Type': 'application/json' } });
              }}
            >
              <Text style={styles.actionButtonText}>🏁 End Simulation</Text>
            </TouchableOpacity>
          </View>
          <Text style={{ fontWeight: '700', color: '#22404D', marginBottom: 12 }}>Trigger Dynamic Scenario Events</Text>
          <View style={{ flexDirection: 'row', flexWrap: 'wrap', marginBottom: 10 }}>
            {['Tornado', 'Power Outage', 'News Flash', 'None'].map(type => (
              <TouchableOpacity
                key={type}
                style={[styles.actionButton, { backgroundColor: selectedIncidentType === type ? '#285F74' : '#f4f6f8', borderWidth: 1, borderColor: '#cad9de', marginRight: 10, marginBottom: 8 }]}
                onPress={() => setSelectedIncidentType(type)}
              >
                <Text style={[styles.actionButtonText, { color: selectedIncidentType === type ? '#fff' : '#22404D' }]}>{type}</Text>
              </TouchableOpacity>
            ))}
          </View>
          <TextInput
            style={[styles.input, { marginBottom: 10 }]}
            value={customIncidentMessage}
            onChangeText={setCustomIncidentMessage}
            placeholder="Custom incident message (optional)"
          />
          <TouchableOpacity
            style={[styles.actionButton, { backgroundColor: '#00A0AF' }]}
            onPress={broadcastIncident}
          >
            <Text style={styles.actionButtonText}>Broadcast Scenario</Text>
          </TouchableOpacity>
        </View>
      )}

    </View>
  );

  const renderStudents = () => (
    <View style={styles.section}>
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>JA BizTown Students</Text>
        <View style={styles.sectionUnderline} />
      </View>
      <View style={styles.card}>
        <View style={styles.tableHeader}>
          <Text style={[styles.tableHeaderText, { flex: 2 }]}>Student Name</Text>
          <Text style={[styles.tableHeaderText, { flex: 1.5 }]}>Job Role</Text>
          <Text style={[styles.tableHeaderText, { flex: 1.5 }]}>Assigned Business</Text>
        </View>
        {students.map((student, index) => {
          const role = roles.find(r => r.roleId === student.roleId);
          const business = businesses.find(b => b.businessId === student.businessId);
          return (
            <View key={student.studentId || index} style={[styles.tableRow, index % 2 === 1 && styles.tableRowAlternate]}>
              <Text style={[styles.tableCell, { flex: 2, fontWeight: '700', color: '#22404D' }]}>
                {student.firstName} {student.lastName}
              </Text>
              <Text style={[styles.tableCell, { flex: 1.5, color: '#285F74' }]}>
                {role?.roleName || 'Unassigned'}
              </Text>
              <Text style={[styles.tableCell, { flex: 1.5 }]}>
                {business?.businessName || 'Waiting Area'}
              </Text>
            </View>
          );
        })}
      </View>
    </View>
  );

  const renderVoting = () => (
    <View style={styles.section}>
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Civic Participation: Voting</Text>
        <View style={styles.sectionUnderline} />
      </View>
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Municipal Election</Text>
        <Text style={styles.cardDescription}>Please cast your vote for the upcoming initiatives in JA BizTown.</Text>
        <View style={{ marginTop: 20 }}>
          <TouchableOpacity style={[styles.actionButton, { marginBottom: 12, backgroundColor: '#f4f6f8', borderWidth: 1, borderColor: '#cad9de' }]}>
            <Text style={[styles.actionButtonText, { color: '#22404D' }]}>Option A: New Town Park</Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.actionButton, { marginBottom: 12, backgroundColor: '#f4f6f8', borderWidth: 1, borderColor: '#cad9de' }]}>
            <Text style={[styles.actionButtonText, { color: '#22404D' }]}>Option B: Technology Hub</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );

  const renderPOS = () => (
    <View style={styles.section}>
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Point of Sale (POS) Terminal</Text>
        <View style={styles.sectionUnderline} />
      </View>
      <View style={[styles.card, { maxWidth: 500, alignSelf: 'center', width: '100%', marginTop: 24 }]}>
        <Text style={[styles.cardTitle, { textAlign: 'center', fontSize: 24 }]}>Checkout</Text>
        <Text style={[styles.cardDescription, { textAlign: 'center' }]}>Process a simulated citizen sale or Tap-to-Pay transfer.</Text>
        
        <View style={{ marginTop: 24, padding: 16, backgroundColor: '#f4f6f8', borderRadius: 8 }}>
          <Text style={{ fontSize: 16, color: '#22404D', fontWeight: 'bold', marginBottom: 8 }}>Item / Service:</Text>
          <TextInput
            style={[styles.input, { marginBottom: 12 }]}
            value={posItemName}
            onChangeText={setPosItemName}
            placeholder="General Merchandise"
          />
          <Text style={{ fontSize: 16, color: '#22404D', fontWeight: 'bold', marginBottom: 8 }}>Sale Amount:</Text>
          <TextInput
            style={[styles.input, { fontSize: 32, textAlign: 'center', padding: 16 }]}
            value={posAmount}
            onChangeText={setPosAmount}
            keyboardType="numeric"
            placeholder="$ 0.00"
          />

          <Text style={{ textAlign: 'center', color: '#5a7a87', marginTop: 10 }}>Tap-to-Pay QR (simulation)</Text>
          <View style={{ alignSelf: 'center', marginTop: 8, width: 120, height: 120, borderWidth: 2, borderColor: '#cad9de', borderStyle: 'dashed', borderRadius: 8, justifyContent: 'center', alignItems: 'center', backgroundColor: '#fff' }}>
            <Text style={{ fontSize: 40, color: '#5a7a87' }}>▦</Text>
          </View>
          
          <TouchableOpacity 
            style={[styles.actionButton, { backgroundColor: '#28a745', marginTop: 16, paddingVertical: 16 }]}
            onPress={handlePosSale}
          >
            <Text style={[styles.actionButtonText, { fontSize: 20 }]}>💳 Process Payment</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );

  const renderIncidentAlert = () => {
    const businessId = currentUser?.businessId;
    const hasDecided = businessContributions[businessId];
    
    return (
      <Modal
        visible={activeIncident !== 'None' && currentUser?.role === 'student' && !hasDecided}
        transparent={true}
        animationType="fade"
      >
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { borderTopWidth: 6, borderTopColor: activeIncident === 'Tornado' ? '#dc3545' : (activeIncident === 'Power Outage' ? '#fd7e14' : '#17a2b8') }]}>
            <Text style={styles.modalIcon}>{activeIncident === 'News Flash' ? '📰' : '🚨'}</Text>
            <Text style={styles.modalTitle}>{activeIncident} Report!</Text>
            <Text style={styles.modalText}>{incidentMessage}</Text>
            <Text style={styles.modalImplication}>
              • Responding will earn your business XP and boost your Civic Score.
              • Ignoring incidents results in a community-engagement penalty.
            </Text>
            
            <View style={styles.modalActions}>
              <TouchableOpacity 
                style={[styles.actionButton, { backgroundColor: '#00A0AF', flex: 1, marginRight: 10 }]}
                onPress={() => handleIncidentDecision('contribute')}
              >
                <Text style={styles.actionButtonText}>Respond</Text>
              </TouchableOpacity>
              <TouchableOpacity 
                style={[styles.actionButton, { backgroundColor: '#f4f6f8', borderWidth: 1, borderColor: '#cad9de', flex: 1 }]}
                onPress={() => handleIncidentDecision('decline')}
              >
                <Text style={[styles.actionButtonText, { color: '#22404D' }]}>Ignore</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    );
  };

  const renderBusinesses = () => (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>🏢 Businesses</Text>
      {businesses.map(business => (
        <TouchableOpacity 
          key={business.businessId} 
          style={[
            styles.card,
            selectedBusinessId === business.businessId && styles.selectedCard
          ]}
          onPress={() => {
            setSelectedBusinessId(business.businessId);
            console.log(`Selected business: ${business.businessName}`);
          }}
        >
          <Text style={styles.cardTitle}>{business.businessName}</Text>
          <Text style={styles.cardSubtitle}>{business.businessType}</Text>
          <Text style={styles.cardDescription}>{business.description}</Text>
          <View style={styles.financialInfo}>
            <Text style={styles.balanceText}>Balance: {formatCurrency(business.currentBalance)}</Text>
            <Text style={styles.capitalText}>Capital: {formatCurrency(business.initialCapital)}</Text>
          </View>
          <View style={styles.statusContainer}>
            <Text style={[styles.statusText, business.isActive ? styles.activeText : styles.inactiveText]}>
              {business.isActive ? 'Active' : 'Inactive'}
            </Text>
          </View>
        </TouchableOpacity>
      ))}
    </View>
  );

  const renderAccounts = () => (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>💳 Bank Accounts</Text>
      {bankAccounts.map((account) => (
        <View key={account.accountId} style={styles.card}>
          <Text style={styles.cardTitle}>{account.accountHolderName}</Text>
          <Text style={styles.cardSubtitle}>Account: {account.accountNumber}</Text>
          <Text style={styles.cardType}>{account.accountType}</Text>
          <View style={styles.financialInfo}>
            <Text style={styles.balanceText}>
              Balance: {formatCurrency(account.balance)}
            </Text>
          </View>
          <View style={styles.statusContainer}>
            <Text style={[styles.statusText, account.isActive ? styles.activeText : styles.inactiveText]}>
              {account.isActive ? '🟢 Active' : '🔴 Inactive'}
            </Text>
          </View>
        </View>
      ))}
    </View>
  );

  const renderTransactions = () => (
    <View style={styles.container}>
      <Text style={styles.viewTitle}>Business Transactions</Text>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {transactions.length === 0 ? (
          <Text style={styles.emptyText}>No transactions recorded yet.</Text>
        ) : (
          transactions.map((transaction, index) => (
            <View key={transaction.transactionId || index} style={styles.transactionCard}>
              <View style={styles.transactionHeader}>
                <Text style={styles.transactionType}>{transaction.transactionType}</Text>
                <Text style={[styles.transactionAmount, { color: transaction.amount < 0 ? '#dc3545' : '#28a745' }]}>
                  {formatCurrency(transaction.amount)}
                </Text>
              </View>
              <View style={styles.transactionDetails}>
                <Text style={styles.transactionDescription}>{transaction.description}</Text>
                <Text style={styles.transactionDate}>{new Date(transaction.transactionDate).toLocaleDateString()}</Text>
              </View>
            </View>
          ))
        )}
      </ScrollView>
    </View>
  );

  const renderLeaderboard = () => (
    <View style={[styles.container, { backgroundColor: '#22404D' }]}>
      <View style={{ padding: 20, alignItems: 'center' }}>
        <Text style={[styles.viewTitle, { color: 'white', fontSize: 32 }]}>🏆 JA BizTown Leaderboard</Text>
        <Text style={{ color: '#E3E24F', fontSize: 18, marginBottom: 20 }}>Live Business Success Rankings</Text>
      </View>
      
      <ScrollView contentContainerStyle={[styles.scrollContent, { paddingHorizontal: 30 }]}>
        {leaderboard.map((entry, index) => (
          <View key={entry.businessId} style={[styles.card, { 
            marginBottom: 15, 
            backgroundColor: index === 0 ? '#E3E24F' : 'white',
            flexDirection: 'row', 
            alignItems: 'center',
            padding: 20,
            borderRadius: 12
          }]}>
            <Text style={{ fontSize: 32, fontWeight: '900', width: 60, color: '#22404D' }}>#{entry.rank}</Text>
            
            <View style={{ flex: 1 }}>
              <Text style={{ fontSize: 22, fontWeight: '800', color: '#22404D' }}>{entry.businessName}</Text>
              <Text style={{ color: '#285F74' }}>{entry.businessType}</Text>
              
              <View style={{ flexDirection: 'row', marginTop: 10 }}>
                <View style={{ marginRight: 15 }}>
                  <Text style={{ fontSize: 10, color: '#285F74' }}>FINANCIAL</Text>
                  <View style={{ height: 6, width: 80, backgroundColor: '#eee', borderRadius: 3, marginTop: 4 }}>
                    <View style={{ height: 6, width: `${(entry.financialScore/400)*100}%`, backgroundColor: '#00A0AF', borderRadius: 3 }} />
                  </View>
                </View>
                <View style={{ marginRight: 15 }}>
                  <Text style={{ fontSize: 10, color: '#285F74' }}>EFFICIENCY</Text>
                  <View style={{ height: 6, width: 80, backgroundColor: '#eee', borderRadius: 3, marginTop: 4 }}>
                    <View style={{ height: 6, width: `${(entry.efficiencyScore/300)*100}%`, backgroundColor: '#28a745', borderRadius: 3 }} />
                  </View>
                </View>
                <View>
                  <Text style={{ fontSize: 10, color: '#285F74' }}>CIVIC</Text>
                  <View style={{ height: 6, width: 80, backgroundColor: '#eee', borderRadius: 3, marginTop: 4 }}>
                    <View style={{ height: 6, width: `${(entry.civicScore/300)*100}%`, backgroundColor: '#fd7e14', borderRadius: 3 }} />
                  </View>
                </View>
              </View>
            </View>
            
            <View style={{ alignItems: 'flex-end' }}>
              <Text style={{ fontSize: 32, fontWeight: '900', color: '#22404D' }}>{entry.totalScore}</Text>
              <Text style={{ fontSize: 12, color: '#285F74' }}>SUCCESS SCORE</Text>
            </View>
          </View>
        ))}
      </ScrollView>
      
      <View style={{ padding: 15, borderTopWidth: 1, borderTopColor: 'rgba(255,255,255,0.1)', alignItems: 'center' }}>
        <Text style={{ color: 'white', fontStyle: 'italic' }}>Presentation Mode Active • Data refreshes in real-time</Text>
      </View>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#007bff" />
        <Text style={styles.loadingText}>Loading JA BizTown...</Text>
      </View>
    );
  }

  if (!isLoggedIn) {
    return renderLogin();
  }

  return (
    <View style={styles.container}>
      {/* JA Header with Logo */}
      <View style={styles.mainHeader}>
        <View style={styles.logoContainer}>
          <Image 
            source={{ uri: '/ja-logo.png' }} 
            style={styles.headerLogoImage}
            resizeMode="contain"
            onError={() => console.log('Logo image failed to load')}
          />
          {/* Fallback text logo */}
          <Text style={styles.headerLogoText}>JA</Text>
        </View>
        <View style={styles.headerNav}>
          <Text style={styles.headerTitle}>JA BizTown</Text>
          <Text style={styles.headerSubtitle}>Education For What's Next™</Text>
        </View>
      </View>

      {error && (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      )}

      {renderNavigation()}

      <ScrollView style={styles.content}>
        {currentView === 'dashboard' && renderDashboard()}
        {currentView === 'businesses' && renderBusinesses()}
        {currentView === 'students' && renderStudents()}
        {currentView === 'voting' && renderVoting()}
        {currentView === 'pos' && renderPOS()}
        {currentView === 'leaderboard' && renderLeaderboard()}
        {currentView === 'accounts' && renderAccounts()}
        {currentView === 'transactions' && renderTransactions()}
        {renderMainFooter()}
      </ScrollView>
      {renderIncidentAlert()}
    </View>
  );
};

const styles = StyleSheet.create({
  // ─── Layout ────────────────────────────────────────────────────────────────
  container: {
    flex: 1,
    backgroundColor: '#f4f6f8',
    fontFamily: 'Montserrat, sans-serif',
  },

  // ─── Loading ───────────────────────────────────────────────────────────────
  loadingText: {
    marginTop: 12,
    fontSize: 16,
    fontFamily: 'Montserrat, sans-serif',
    fontWeight: '600',
    color: '#285F74',
  },

  // ─── Error ─────────────────────────────────────────────────────────────────
  errorContainer: {
    backgroundColor: '#fde8e8',
    padding: 15,
    margin: 10,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#dc3545',
  },
  errorText: {
    color: '#721c24',
    fontFamily: 'Montserrat, sans-serif',
    fontSize: 14,
  },

  // ─── Main Header ───────────────────────────────────────────────────────────
  header: {
    backgroundColor: '#22404D',
    padding: 20,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
    elevation: 5,
  },
  mainHeader: {
    backgroundColor: '#22404D',
    paddingVertical: 14,
    paddingHorizontal: 20,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
    elevation: 5,
  },
  logoContainer: {
    alignItems: 'flex-start',
    flex: 1,
  },
  headerLogoImage: {
    width: 120,
    height: 40,
    resizeMode: 'contain',
  },
  headerLogoText: {
    fontSize: 26,
    fontWeight: '800',
    fontFamily: 'Montserrat, sans-serif',
    color: '#ffffff',
    backgroundColor: '#285F74',
    paddingHorizontal: 14,
    paddingVertical: 6,
    borderRadius: 6,
  },
  headerNav: {
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '700',
    fontFamily: 'Montserrat, sans-serif',
    color: '#ffffff',
    letterSpacing: 0.5,
  },
  headerSubtitle: {
    fontSize: 13,
    fontFamily: 'Montserrat, sans-serif',
    color: '#E3E24F',
    fontStyle: 'italic',
    marginTop: 2,
  },

  // ─── Navigation Bar ────────────────────────────────────────────────────────
  navigationBar: {
    flexDirection: 'row',
    backgroundColor: '#ffffff',
    paddingVertical: 10,
    paddingHorizontal: 10,
    borderBottomWidth: 3,
    borderBottomColor: '#285F74',
    flexWrap: 'wrap',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 4,
    elevation: 4,
  },
  navButton: {
    backgroundColor: '#f4f6f8',
    paddingVertical: 10,
    paddingHorizontal: 16,
    margin: 4,
    borderRadius: 8,
    minWidth: 100,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#d0dde3',
  },
  navButtonActive: {
    backgroundColor: '#285F74',
    borderColor: '#285F74',
  },
  navButtonText: {
    fontSize: 13,
    fontWeight: '700',
    fontFamily: 'Montserrat, sans-serif',
    color: '#22404D',
  },
  navButtonTextActive: {
    color: '#ffffff',
  },
  logoutButton: {
    backgroundColor: '#dc3545',
    paddingVertical: 10,
    paddingHorizontal: 16,
    margin: 4,
    borderRadius: 8,
    minWidth: 100,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#c82333',
    marginLeft: 'auto',
  },
  logoutButtonText: {
    fontSize: 13,
    fontWeight: '700',
    fontFamily: 'Montserrat, sans-serif',
    color: '#ffffff',
  },

  // ─── Content / Sections ────────────────────────────────────────────────────
  content: {
    flex: 1,
    padding: 16,
    backgroundColor: '#f4f6f8',
  },
  section: {
    marginBottom: 28,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: '800',
    fontFamily: 'Montserrat, sans-serif',
    marginBottom: 18,
    color: '#22404D',
    borderBottomWidth: 3,
    borderBottomColor: '#E3E24F',
    paddingBottom: 10,
    textTransform: 'uppercase',
    letterSpacing: 0.8,
  },

  // ─── Cards ─────────────────────────────────────────────────────────────────
  card: {
    backgroundColor: '#ffffff',
    padding: 20,
    marginBottom: 14,
    borderRadius: 10,
    shadowColor: '#22404D',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.08,
    shadowRadius: 6,
    elevation: 4,
    borderLeftWidth: 4,
    borderLeftColor: '#00A0AF',
    borderWidth: 1,
    borderColor: '#e0eaed',
  },
  selectedCard: {
    borderLeftWidth: 4,
    borderLeftColor: '#285F74',
    borderWidth: 2,
    borderColor: '#285F74',
    shadowOpacity: 0.18,
    shadowRadius: 8,
    elevation: 8,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '700',
    fontFamily: 'Montserrat, sans-serif',
    color: '#22404D',
    marginBottom: 6,
  },
  cardSubtitle: {
    fontSize: 14,
    fontFamily: 'Montserrat, sans-serif',
    color: '#5a7a87',
    marginBottom: 10,
    fontStyle: 'italic',
  },
  cardDescription: {
    fontSize: 14,
    fontFamily: 'Montserrat, sans-serif',
    color: '#4a5568',
    marginBottom: 14,
    lineHeight: 22,
  },
  cardType: {
    fontSize: 12,
    fontFamily: 'Montserrat, sans-serif',
    color: '#285F74',
    fontWeight: '700',
    marginBottom: 8,
    textTransform: 'uppercase',
    letterSpacing: 0.8,
  },
  financialInfo: {
    borderTopWidth: 1,
    borderTopColor: '#e0eaed',
    paddingTop: 14,
    marginTop: 10,
  },
  balanceText: {
    fontSize: 17,
    fontWeight: '700',
    fontFamily: 'Montserrat, sans-serif',
    color: '#1a7a4e',
    marginBottom: 6,
  },
  capitalText: {
    fontSize: 14,
    fontFamily: 'Montserrat, sans-serif',
    color: '#5a7a87',
  },

  // ─── Dashboard ─────────────────────────────────────────────────────────────
  welcomeText: {
    fontSize: 22,
    fontWeight: '800',
    fontFamily: 'Montserrat, sans-serif',
    color: '#22404D',
    marginBottom: 6,
  },
  roleText: {
    fontSize: 15,
    fontFamily: 'Montserrat, sans-serif',
    color: '#5a7a87',
    marginBottom: 22,
    textTransform: 'capitalize',
  },
  statsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 22,
  },
  statCard: {
    backgroundColor: '#ffffff',
    padding: 20,
    borderRadius: 12,
    width: '48%',
    marginBottom: 14,
    alignItems: 'center',
    shadowColor: '#22404D',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.09,
    shadowRadius: 6,
    elevation: 4,
    borderTopWidth: 4,
    borderTopColor: '#E3E24F',
    borderWidth: 1,
    borderColor: '#e0eaed',
    cursor: 'pointer',
  },
  statNumber: {
    fontSize: 34,
    fontWeight: '800',
    fontFamily: 'Montserrat, sans-serif',
    color: '#285F74',
    marginBottom: 6,
  },
  statLabel: {
    fontSize: 13,
    fontFamily: 'Montserrat, sans-serif',
    color: '#5a7a87',
    textAlign: 'center',
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  totalBalanceContainer: {
    backgroundColor: '#285F74',
    padding: 24,
    borderRadius: 12,
    alignItems: 'center',
    shadowColor: '#22404D',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 6,
  },
  totalBalanceLabel: {
    fontSize: 15,
    fontFamily: 'Montserrat, sans-serif',
    fontWeight: '600',
    color: '#E3E24F',
    marginBottom: 8,
    textTransform: 'uppercase',
    letterSpacing: 0.8,
  },
  totalBalanceAmount: {
    fontSize: 32,
    fontWeight: '800',
    fontFamily: 'Montserrat, sans-serif',
    color: '#ffffff',
  },

  // ─── Transaction ──────────────────────────────────────────────────────────
  transactionInfo: {
    borderTopWidth: 1,
    borderTopColor: '#e0eaed',
    paddingTop: 14,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  amountText: {
    fontSize: 16,
    fontWeight: '700',
    fontFamily: 'Montserrat, sans-serif',
    color: '#1a7a4e',
  },
  dateText: {
    fontSize: 13,
    fontFamily: 'Montserrat, sans-serif',
    color: '#5a7a87',
  },

  // ─── Status ───────────────────────────────────────────────────────────────
  statusContainer: {
    marginTop: 14,
  },
  statusText: {
    fontSize: 13,
    fontWeight: '700',
    fontFamily: 'Montserrat, sans-serif',
  },
  activeText: {
    color: '#1a7a4e',
  },
  inactiveText: {
    color: '#dc3545',
  },

  // ─── Tabs ─────────────────────────────────────────────────────────────────
  tabContainer: {
    backgroundColor: '#f4f6f8',
    borderRadius: 12,
    margin: 15,
    overflow: 'hidden',
  },
  tabBar: {
    flexDirection: 'row',
    backgroundColor: '#ffffff',
    borderBottomWidth: 3,
    borderBottomColor: '#285F74',
  },
  tab: {
    flex: 1,
    paddingVertical: 14,
    alignItems: 'center',
    backgroundColor: '#f4f6f8',
    borderRightWidth: 1,
    borderRightColor: '#e0eaed',
  },
  tabActive: {
    backgroundColor: '#22404D',
    borderBottomWidth: 3,
    borderBottomColor: '#E3E24F',
  },
  tabText: {
    fontSize: 13,
    fontWeight: '600',
    fontFamily: 'Montserrat, sans-serif',
    color: '#5a7a87',
  },
  tabTextActive: {
    fontSize: 13,
    fontWeight: '700',
    fontFamily: 'Montserrat, sans-serif',
    color: '#E3E24F',
  },
  tabContent: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  tabPanel: {
    padding: 20,
  },
  tabPanelTitle: {
    fontSize: 18,
    fontWeight: '700',
    fontFamily: 'Montserrat, sans-serif',
    color: '#22404D',
    marginBottom: 18,
    borderBottomWidth: 3,
    borderBottomColor: '#E3E24F',
    paddingBottom: 10,
  },

  // ─── Login ────────────────────────────────────────────────────────────────
  loginContainer: {
    flex: 1,
    position: 'relative',
    backgroundColor: '#f4f6f8',
  },
  loginBackground: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: '#22404D',
  },
  loginOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: '#22404D',
    opacity: 0.04,
  },
  loginContent: {
    flex: 1,
    width: '100%',
    position: 'relative',
    zIndex: 1,
  },
  loginScrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 32,
  },
  logoSection: {
    alignItems: 'center',
    marginBottom: 36,
  },
  logoCircle: {
    width: 88,
    height: 88,
    borderRadius: 44,
    backgroundColor: '#22404D',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 14,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 10,
    elevation: 10,
    borderWidth: 4,
    borderColor: '#E3E24F',
  },
  logoText: {
    fontSize: 30,
    fontWeight: '800',
    fontFamily: 'Montserrat, sans-serif',
    color: '#ffffff',
  },
  logoSubtitle: {
    fontSize: 18,
    fontWeight: '700',
    fontFamily: 'Montserrat, sans-serif',
    color: '#ffffff',
    marginBottom: 4,
  },
  logoDescription: {
    fontSize: 13,
    fontFamily: 'Montserrat, sans-serif',
    color: '#dce9ed',
    textAlign: 'center',
    fontStyle: 'italic',
  },
  welcomeSection: {
    alignItems: 'center',
    marginBottom: 36,
  },
  welcomeTitle: {
    fontSize: 30,
    fontWeight: '800',
    fontFamily: 'Montserrat, sans-serif',
    color: '#ffffff',
    marginBottom: 12,
    textAlign: 'center',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  welcomeDescription: {
    fontSize: 15,
    fontFamily: 'Montserrat, sans-serif',
    color: '#dce9ed',
    textAlign: 'center',
    lineHeight: 24,
    maxWidth: 420,
  },
  roleSection: {
    width: '100%',
    maxWidth: 520,
  },
  sectionHeader: {
    marginBottom: 24,
    position: 'relative',
  },
  sectionTitle: {
    fontSize: 26,
    fontWeight: '800',
    fontFamily: 'Montserrat, sans-serif',
    color: '#22404D',
    letterSpacing: 0.5,
  },
  sectionUnderline: {
    width: 60,
    height: 4,
    backgroundColor: '#E3E24F',
    marginTop: 8,
    borderRadius: 2,
  },
  roleSectionTitle: {
    fontSize: 16,
    fontWeight: '700',
    fontFamily: 'Montserrat, sans-serif',
    color: '#E3E24F',
    marginBottom: 22,
    textAlign: 'center',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  roleCard: {
    backgroundColor: '#ffffff',
    borderRadius: 14,
    marginBottom: 16,
    flexDirection: 'row',
    alignItems: 'center',
    shadowColor: '#22404D',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 10,
    elevation: 6,
    borderWidth: 1,
    borderColor: '#dce9ed',
    overflow: 'hidden',
  },
  studentLoginCard: {
    backgroundColor: '#ffffff',
    borderRadius: 14,
    borderWidth: 1,
    borderColor: '#dce9ed',
    borderLeftWidth: 5,
    borderLeftColor: '#00A0AF',
    padding: 18,
    width: '100%',
    maxWidth: 520,
  },
  loginFieldLabel: {
    fontSize: 13,
    fontFamily: 'Montserrat, sans-serif',
    color: '#22404D',
    marginBottom: 6,
    fontWeight: '700',
  },
  loginFieldInput: {
    borderWidth: 1,
    borderColor: '#cad9de',
    backgroundColor: '#ffffff',
    borderRadius: 8,
    paddingVertical: 12,
    paddingHorizontal: 12,
    color: '#22404D',
    marginBottom: 14,
    width: '100%',
  },
  studentLoginButton: {
    paddingVertical: 12,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#00A0AF',
    width: '100%',
    marginTop: 4,
  },
  studentRole: {
    borderLeftWidth: 5,
    borderLeftColor: '#285F74',
  },
  teacherRole: {
    borderLeftWidth: 5,
    borderLeftColor: '#00A0AF',
  },
  adminRole: {
    borderLeftWidth: 5,
    borderLeftColor: '#E3E24F',
  },
  roleIcon: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: '#f0f7f9',
    justifyContent: 'center',
    alignItems: 'center',
    margin: 16,
  },
  roleIconText: {
    fontSize: 26,
  },
  roleContent: {
    padding: 16,
    flex: 1,
  },
  roleInfo: {
    padding: 16,
    flex: 1,
  },
  roleTitle: {
    fontSize: 18,
    fontWeight: '700',
    fontFamily: 'Montserrat, sans-serif',
    color: '#22404D',
    marginBottom: 6,
  },
  roleDescription: {
    fontSize: 13,
    fontFamily: 'Montserrat, sans-serif',
    color: '#5a7a87',
    lineHeight: 20,
  },
  loginFooter: {
    marginTop: 40,
    marginBottom: 24,
    alignItems: 'center',
    width: '100%',
  },
  footerText: {
    fontSize: 12,
    fontFamily: 'Montserrat, sans-serif',
    color: '#dce9ed',
  },
  footerSubtext: {
    fontSize: 11,
    fontFamily: 'Montserrat, sans-serif',
    color: '#a0aec0',
    marginTop: 4,
    fontStyle: 'italic',
  },

  // ─── Main Footer ──────────────────────────────────────────────────────────
  footer: {
    backgroundColor: '#22404D',
    padding: 20,
    alignItems: 'center',
  },
  mainFooter: {
    backgroundColor: '#22404D',
    paddingTop: 36,
  },
  footerSection: {
    alignItems: 'center',
    marginBottom: 28,
    paddingHorizontal: 20,
  },
  footerTitle: {
    fontSize: 18,
    fontWeight: '700',
    fontFamily: 'Montserrat, sans-serif',
    color: '#E3E24F',
    marginBottom: 18,
    textAlign: 'center',
  },
  footerLinks: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    marginBottom: 20,
  },
  footerLink: {
    backgroundColor: 'rgba(255,255,255,0.08)',
    paddingVertical: 10,
    paddingHorizontal: 14,
    borderRadius: 6,
    margin: 5,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.15)',
  },
  footerLinkText: {
    fontSize: 13,
    fontWeight: '600',
    fontFamily: 'Montserrat, sans-serif',
    color: '#ffffff',
    textAlign: 'center',
  },
  footerBottom: {
    alignItems: 'center',
    backgroundColor: '#00A0AF',
    paddingVertical: 18,
    paddingHorizontal: 20,
    borderTopWidth: 2,
    borderTopColor: 'rgba(255,255,255,0.2)',
  },
  footerCopy: {
    fontSize: 12,
    fontFamily: 'Montserrat, sans-serif',
    color: '#ffffff',
    marginBottom: 4,
    fontWeight: '600',
  },
  footerMission: {
    fontSize: 13,
    fontFamily: 'Montserrat, sans-serif',
    color: 'rgba(255,255,255,0.85)',
    fontStyle: 'italic',
    textAlign: 'center',
  },
  footerLinksRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 10,
    flexWrap: 'wrap',
  },
  footerSmallLink: {
    marginHorizontal: 8,
    marginVertical: 3,
  },
  footerSmallText: {
    fontSize: 11,
    fontFamily: 'Montserrat, sans-serif',
    color: 'rgba(255,255,255,0.8)',
  },
  actionButton: {
    paddingVertical: 12,
    paddingHorizontal: 22,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
    elevation: 3,
    minWidth: 140,
  },
  actionButtonText: {
    color: '#ffffff',
    fontSize: 13,
    fontWeight: '700',
    fontFamily: 'Montserrat, sans-serif',
    textTransform: 'uppercase',
    letterSpacing: 0.8,
  },
  input: {
    borderWidth: 1,
    borderColor: '#cad9de',
    backgroundColor: '#ffffff',
    borderRadius: 8,
    paddingVertical: 10,
    paddingHorizontal: 12,
    color: '#22404D',
    marginBottom: 12,
  },
  tableHeader: {
    flexDirection: 'row',
    backgroundColor: '#f8fafb',
    paddingVertical: 14,
    paddingHorizontal: 16,
    borderBottomWidth: 2,
    borderBottomColor: '#285F74',
    borderTopLeftRadius: 8,
    borderTopRightRadius: 8,
  },
  tableHeaderText: {
    fontSize: 13,
    fontWeight: '800',
    color: '#22404D',
    fontFamily: 'Montserrat, sans-serif',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  tableRow: {
    flexDirection: 'row',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#eef2f4',
    alignItems: 'center',
  },
  tableRowAlternate: {
    backgroundColor: '#f9fcfe',
  },
  tableCell: {
    fontSize: 14,
    color: '#415a63',
    fontFamily: 'Montserrat, sans-serif',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(34, 64, 77, 0.9)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  modalContent: {
    backgroundColor: '#ffffff',
    borderRadius: 16,
    padding: 30,
    width: '100%',
    maxWidth: 500,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.25,
    shadowRadius: 15,
    elevation: 10,
  },
  modalIcon: {
    fontSize: 50,
    marginBottom: 20,
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: '800',
    color: '#22404D',
    fontFamily: 'Montserrat, sans-serif',
    marginBottom: 16,
    textAlign: 'center',
  },
  modalText: {
    fontSize: 16,
    color: '#4a5568',
    fontFamily: 'Montserrat, sans-serif',
    lineHeight: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  modalImplication: {
    fontSize: 14,
    color: '#5a7a87',
    fontFamily: 'Montserrat, sans-serif',
    fontStyle: 'italic',
    marginBottom: 24,
    backgroundColor: '#f8fafb',
    padding: 12,
    borderRadius: 8,
    width: '100%',
  },
  modalActions: {
    flexDirection: 'row',
    width: '100%',
  },
});

export default App;

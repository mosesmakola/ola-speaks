import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { createStackNavigator } from '@react-navigation/stack';
import { NavigationContainer } from '@react-navigation/native';
import LottieView from "lottie-react-native";
import { useState, useEffect, useRef } from 'react';

// Home Screen Component
function HomeScreen({ navigation }) {
  const [introSentence, setIntroSentence] = useState("");
  const [displayText, setDisplayText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const fullTextRef = useRef("");
  const timerRef = useRef(null);
  
  // Fetch random sentence from API
  const fetchRandomSentence = async () => {
    try {
      // Your API URL
      const response = await fetch('http://172.20.10.4:1111/randomTranslation');
      const data = await response.json();
      
      // Store the new sentence and start typing animation
      fullTextRef.current = data.introductionSentence;
      setDisplayText("");
      setIsTyping(true);
    } catch (error) {
      console.error('Error fetching random sentence:', error);
      fullTextRef.current = "Hi I'm Ola! Can I speak in your language?";
      setDisplayText("");
      setIsTyping(true);
    }
  };

  // Setup interval to fetch new sentence every 10 seconds
  useEffect(() => {
    // Fetch on initial load
    fetchRandomSentence();
    
    // Set up timer for refreshing every 10 seconds
    timerRef.current = setInterval(() => {
      fetchRandomSentence();
    }, 10000);
    
    // Clean up on unmount
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  // Handle typing animation
  useEffect(() => {
    let typingTimer;
    
    if (isTyping && displayText.length < fullTextRef.current.length) {
      typingTimer = setTimeout(() => {
        setDisplayText(fullTextRef.current.substring(0, displayText.length + 1));
      }, 50); // Speed of typing (lower = faster)
    } else if (displayText.length === fullTextRef.current.length) {
      setIsTyping(false);
    }
    
    return () => {
      if (typingTimer) clearTimeout(typingTimer);
    };
  }, [isTyping, displayText]);

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerText}>OLA</Text>
      </View>
      
      {/* Lottie Animation */}
      <View style={styles.animationContainer}>
        <LottieView
          source={require("./assets/ola_gradient.json")}
          autoPlay
          loop
          speed={2}
          style={styles.olaGradient}
        />
      </View>
      
      {/* Text Container */}
      <View style={styles.textContainer}>
        <Text style={styles.introText}>{displayText}</Text>
        {isTyping && <Text style={styles.cursor}>|</Text>}
      </View>
      
      {/* Button */}
      <TouchableOpacity 
        style={styles.button}
        onPress={() => navigation.navigate('SecondScreen')}
      >
        <Text style={styles.buttonText}>GET STARTED</Text>
      </TouchableOpacity>
      
      <StatusBar style="light" />
    </View>
  );
}

// Second Screen Component (placeholder)
function SecondScreen() {
  return (
    <View style={styles.secondScreenContainer}>
      <Text style={styles.secondScreenText}>Welcome to Ola!</Text>
      <Text style={styles.secondScreenSubtext}>Your language learning journey begins here.</Text>
    </View>
  );
}

// Stack Navigator
const Stack = createStackNavigator();

// Main App Component
export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator 
        initialRouteName="Home"
        screenOptions={{
          headerShown: false
        }}
      >
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="SecondScreen" component={SecondScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8805B',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 50,
  },
  header: {
    width: '100%',
    paddingTop: 40,
    alignItems: 'center',
  },
  headerText: {
    fontSize: 55,
    fontWeight: 'bold',
    color: 'rgba(255,255,255,0.7)',
    letterSpacing: 4,
  },
  animationContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  olaGradient: {
    width: 400,
    height: 400,
    shadowColor: "black",
    shadowOffset: {width: 1, height: 1},
    shadowOpacity: 0.09,
    shadowRadius: 10,
  },
  textContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: 80,
    paddingHorizontal: 30,
    marginBottom: 40,
  },
  introText: {
    fontSize: 20,
    fontWeight: '500',
    lineHeight: 50,
    textAlign: 'center',
    color: 'rgba(255,255,255,0.7)',  
    lineHeight: 28,
  },
  cursor: {
    color: 'white',
    fontSize: 20,
    fontWeight: '500',
  },
  button: {
    backgroundColor: 'rgba(255,255,255,0.7)',
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 10,
    marginBottom: 30,
    shadowColor: "rgba(0,0,0,0.2)",
    shadowOffset: {width: 0, height: 3},
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 5,
  },
  buttonText: {
    color: '#F8805B',
    fontSize: 18,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  secondScreenContainer: {
    flex: 1,
    backgroundColor: '#F8805B',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  secondScreenText: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 20,
  },
  secondScreenSubtext: {
    fontSize: 18,
    color: 'white',
    textAlign: 'center',
  }
});
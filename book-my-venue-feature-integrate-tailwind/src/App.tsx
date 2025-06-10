import { Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import HomePage from "./pages/HomePage";

import "./App.css";
import LoginPage from "./pages/LoginPage";
import MainLayout from "./components/Layout/MainLayout";
import DashboardLayout from "./components/Layout/DashboardLayout";
import VenueDashboard from "./components/Dashboard Components/VenueDashboard";
import VendorDashboard from "./components/Dashboard Components/VendorDashboard";
import ServicesDashboard from "./components/Dashboard Components/ServicesDashboard";
import DashboardPage from "./pages/DashboardPage";
import AboutUs from "./pages/AboutUs";
import ContactUs from "./pages/ContactUs";
import RegisterPage from "./pages/RegisterPage";

const queryClient = new QueryClient();  

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Routes>
        <Route element={<MainLayout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutUs />} />
          <Route path="/services" element={<div>Services</div>} />
          <Route path="/contact" element={<ContactUs />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/venues" element={<div>Venues</div>} />
          <Route path="/venues/:id" element={<div>Venue Details</div>} />
        </Route>

      {/* Dashboard Pages */}
      <Route path="/dashboard" element={<DashboardLayout />}>
          <Route path="dashboardpage" element={<DashboardPage />} />
          <Route path="venue" element={<VenueDashboard />} />
          <Route path="Vendors" element={<VendorDashboard />} />
          <Route path="Services" element={<ServicesDashboard />} />

      </Route>

      </Routes>
    </QueryClientProvider>
  );
}

export default App;

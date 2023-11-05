import { useState } from "react";
import React from "react";
import { useNavigate } from "react-router-dom";
import "./AppBar.css";

const AppBar = () => {
	const navigate = useNavigate();
	const [activeTab, setActiveTab] = useState(0);
	
	const handleTabClick = (index) => {
		setActiveTab(index);
		switch (index) {
			case 0:
				navigate("/timeline");
				break;
			case 1:
				navigate("/overview");
				break;
			default:
				break;
		}
	};
	
	
	return (
		<div className="app-bar">
			<Tabs activeTab={activeTab} onTabClick={handleTabClick}>
				<Tab label="TIMELINE" />
				<Tab label="OVERVIEW" />
			</Tabs>
		</div>
	);
};

const Tabs = ({ activeTab, onTabClick, children }) => {
	return (
		<div className="tabs">
			{React.Children.map(children, (child, index) => {
				return React.cloneElement(child, {
					active: index === activeTab,
					onClick: () => onTabClick(index),
				});
			})}
		</div>
	);
};

const Tab = ({ label, active, onClick }) => {
	return (
		<div
			className={`tab ${active ? "active" : ""}`}
			onClick={onClick}
		>
			{label}
		</div>
	);
};

export default AppBar;

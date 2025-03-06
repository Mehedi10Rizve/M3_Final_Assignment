from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from llm_config import llm
from serper_config import get_serper_api_key


@CrewBase
class CareerCrew:
    """Crew that provides career guidance and job market insights"""

    agents_config = "config/agents.yaml" # Loading agent and task configurations from YAML files
    tasks_config = "config/tasks.yaml"

    @agent
    def career_advisor(self) -> Agent:
        """AI Career Advisor - suggests career paths based on user input"""
        return Agent(
            config=self.agents_config["career_advisor"], # Load career advisor config
            llm=llm, # Using the configured LLM model
            verbose=True, # Enabling logging for debugging
        )

    @agent
    def job_market_analyst(self) -> Agent:
        """AI Job Market Analyst - fetches real job data"""
        search_tool = SerperDevTool(api_key=get_serper_api_key()) # Initialize search tool
        return Agent(
            config=self.agents_config["job_market_analyst"],
            llm=llm, # Use the configured LLM model
            tools=[search_tool], # Provide search capability
            verbose=True, # Enable logging
        )

    def career_guidance(self, skills: str, interests: str) -> Task:
        """Task: Provide personalized career suggestions based on user input"""
        return Task(
            config=self.tasks_config["career_guidance"], # Load task configuration
            agent=self.career_advisor(), # Assign career advisor agent
            inputs={"skills": skills, "interests": interests},  # Pass user input
            output_key="career_suggestion", # Define output key for chaining tasks
        )

    def job_market_analysis(self, career_suggestion: str) -> Task:
        """Task: Analyze job demand, salaries & skills for the given career"""
        return Task(
            config=self.tasks_config["job_market_insights"], # Load task configuration
            agent=self.job_market_analyst(), # Assign job market analyst agent
            inputs={"career_suggestion": career_suggestion},  # Use career suggestion as input
        )

    @crew
    def career_crew(self, skills: str, interests: str) -> Crew:
        """Creates and executes the Career Guidance Crew"""

        # Step 1: Get career suggestions from Career Advisor
        career_task = self.career_guidance(skills, interests)

        # Step 2: Wait for `career_task.output` before passing it to Job Market Analyst
        job_task = self.job_market_analysis(career_task.output)

        return Crew(
            agents=[self.career_advisor(), self.job_market_analyst()],
            tasks=[career_task, job_task],
            process=Process.sequential,  # Ensures job_task waits for career_task
            verbose=True,
        )


if __name__ == "__main__":
    # Get user input
    skills = input("Enter your skills: ").strip()
    interests = input("Enter your interests: ").strip()

    # Call the crew with user input
    careercrew = CareerCrew().career_crew(skills, interests)  
    results = careercrew.kickoff()

    results_str = str(results)

    # Print and save results
    print("\n🔹 Career Guidance & Job Market Insights 🔹\n")
    print(results_str)

    with open("career_guidance_results.md", "w", encoding="utf-8") as f:
        f.write("# Career Guidance & Job Market Insights\n\n")
        f.write(results_str)
    
    print("\n✅ Results saved to 'career_guidance_results.md'")

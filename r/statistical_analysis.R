args <- commandArgs(trailingOnly = TRUE)
input_path <- args[1]
output_path <- args[2]

data <- read.csv(input_path)
data <- data[!is.na(data$mean_assignment_score), ]

correlation_clicks <- cor.test(data$total_clicks, data$mean_assignment_score)
correlation_attendance <- cor.test(data$attendance_rate, data$mean_assignment_score)

model <- lm(mean_assignment_score ~ total_clicks + total_posts + attendance_rate, data = data)
model_summary <- summary(model)

output_lines <- c(
  "R Statistical Analysis",
  "=======================",
  "",
  sprintf("Pearson correlation (total_clicks vs mean_assignment_score): r=%.4f, p=%.4g",
          correlation_clicks$estimate, correlation_clicks$p.value),
  sprintf("Pearson correlation (attendance_rate vs mean_assignment_score): r=%.4f, p=%.4g",
          correlation_attendance$estimate, correlation_attendance$p.value),
  "",
  "Linear regression: mean_assignment_score ~ total_clicks + total_posts + attendance_rate",
  sprintf("R-squared: %.4f", model_summary$r.squared),
  sprintf("Adjusted R-squared: %.4f", model_summary$adj.r.squared)
)

writeLines(output_lines, output_path)

radius_calc <- function(dist_to_ball){
  # can be changed to better map NFL
  return(4 + (dist_to_ball>=15) * 6 + (dist_to_ball<15) * dist_to_ball^3/560)
}

deg2rad <- function(deg) {(deg * pi) / (180)}

compute_influence <- function(x_point, y_point, x0, y0, x, y, s, o){
  # all input must be numeric (i.e. does not contain matrix / vector)
  
  point = c(x_point, y_point)
  ball_coords = c(x0, y0)
  player_coords = c(x, y)
  dist_to_ball = sqrt((x-x0)^2 + (y-y0)^2)
  radius = radius_calc(dist_to_ball)
  theta = deg2rad(o)
  s_ratio = (s/13)^2 # set max speed to be 13m/s
  
  # %*% = dot product
  # solve() finds the inverse of a matrix
  # t() finds the transpose of a matrix / vector
  s_matrix = matrix(c(radius*(1+s_ratio), 0, 0, radius*(1-s_ratio)), nrow = 2, ncol = 2, byrow = TRUE)
  r_matrix = matrix(c(cos(theta), -sin(theta), sin(theta), cos(theta)), nrow = 2, ncol = 2, byrow = TRUE)
  cov_matrix = ((r_matrix %*% s_matrix) %*% s_matrix) %*% solve(r_matrix)
  
  norm_fact = (1/2*pi) * (1/sqrt(det(cov_matrix)))
  mu_play = player_coords + s * c(cos(theta), sin(theta)) / 2
  
  intermed_scalar_player = ((player_coords - mu_play) %*% solve(cov_matrix)) %*% t(t(player_coords - mu_play))
  intermed_scalar_point = ((point - mu_play) %*% solve(cov_matrix)) %*% t(t(point - mu_play))
  player_influence = norm_fact * exp(-0.5 * intermed_scalar_player[1, 1])
  point_influence = norm_fact * exp(-0.5 * intermed_scalar_point[1, 1])
  
  return(point_influence / player_influence)
}

# Test
# compute_influence(45, 45, 30, 30, 25, 25, 10, 270)
-- Lua: tabeller, funksjoner, metatabeller og løkker
local G <const> = 6.674e-11
local Legeme = {}
Legeme.__index = Legeme

--[[ Blokkommentar
     over flere linjer ]]
function Legeme.ny(navn, masse)
  local self = setmetatable({}, Legeme)
  self.navn = navn or "ukjent"
  self.masse = masse or 1.0
  return self
end

function Legeme:kraft(annen, r)
  if r == 0 then error("avstand null: " .. self.navn) end
  return G * self.masse * annen.masse / r ^ 2
end

local planeter = { Legeme.ny("Jorda", 5.972e24), Legeme.ny("Mars", 6.4e23) }
for i, p in ipairs(planeter) do
  print(string.format("%d %s %.2e\n", i, p.navn, p.masse))
end
for k = 1, 10, 2 do if k % 3 == 0 then goto videre end ::videre:: end
while true do break end
local bits, heltall = (0xFF & 0x0F) | 1 << 2 ~ 3, 7 // 2
repeat local x = #planeter until x > 0 and not nil
local tekst = [[
Lang streng
over linjer]]
local ok, feil = pcall(function(...) return select("#", ...) end, 1, 2)
return Legeme

-- Vanskelige tilfeller: metametoder, varargs, strenger, lukninger og operatorer
local Vektor = setmetatable({}, { __call = function(kl, x, y) return setmetatable({ x = x or 0, y = y or 0 }, kl) end })
Vektor.__index = Vektor
Vektor.__add = function(a, b) return Vektor(a.x + b.x, a.y + b.y) end
Vektor.__mul = function(a, k) return Vektor(a.x * k, a.y * k) end
Vektor.__unm = function(a) return Vektor(-a.x, -a.y) end
Vektor.__eq = function(a, b) return a.x == b.x and a.y == b.y end
Vektor.__tostring = function(v) return ("(%g, %g)"):format(v.x, v.y) end
Vektor.__len = function(v) return 2 end
Vektor.__concat = function(a, b) return tostring(a) .. tostring(b) end
local function vanskelig(navn, ...)
  local t <close> = nil; local antall <const> = select("#", ...); local første, resten = ...
  local n = 0; n = n + 1; n = n - 2; n = n * 3; n = n // 4; n = n % 5; n = n ^ 2; n = n << 1 | 1 ~ 2 & ~3 >> 1
  local lik = n == 1 or n ~= 1 and not (n < 2) or n <= 2 and n >= -1; local neg = -n + #navn % 2 ^ 3
  local v = Vektor(1, 2) + Vektor(3, 4) * 2 + -Vektor(); lik = lik and v == v and #v == 2 and tostring(v .. v) ~= ""
  local tekst = "a + b == c " .. (navn or "ukjent") .. ' apostrof \'x\' ' .. [[rå \n]] .. [==[med ]] inni]==] .. "\t\u{E6}\65"
  for i = 10, 1, -2 do if i % 3 == 0 then goto neste elseif i > 7 then break end ::neste:: end
  local teller = (function() local c = 0; return function() c = c + 1; return c end end)()
  while teller() < 3 do end; repeat n = n - 1 until n <= 0
  return antall + (første or 0) + (resten and 1 or 0) + neg + #tekst + teller(), ...
end

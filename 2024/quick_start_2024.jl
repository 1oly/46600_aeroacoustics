using HDF5, AeroAcoustics, Plots
# The AeroAcoustics.jl package is structured around the struct `Environment`, that takes all neccessary variables associated with an acoustic image as input. 
# We will use the measurement data in the `data` folder. 
# These files are cross-spectral matrices (csm), a frequency domain representation of the measurement.

# Open the hdf5 file from the /data directory and assemble the data to a Complex array.
csm_file = joinpath(pwd(),"..","data","NACA63018_u0_80mps_aoa_0_clean.h5")
csm_ref = h5open(csm_file, "r") do file
    read(file, "CsmData/csmReal")+im*read(file, "CsmData/csmImag")
end

# Get the associated frequencies, and microphone array geometry:
fc = h5read(csm_file, "CsmData")["binCenterFrequenciesHz"]
micgeom = h5read(csm_file, "CsmData")["arrayGeom"]

# We are now ready populate the `Environment` struct. 
# The measurement distance `z0`, the microphone geometry `micgeom`, and the csm `CSM` are required variables.
# First, the csm is constructed as a FreqArray, which holds the array and associated frequency bins:
CSM = FreqArray(csm_ref,fc)

# The distance between source and receiver plane is
z0 = 2.3 

# Let's also define the expected source position (TE noise) and a region of integration:
src_pos = (0.05,0.05)
dxdy = (0.5,0.8)
int_region = AeroAcoustics.point_to_region(src_pos,dxdy)

# The Environment is defined:
E = Environment(
    z0 = z0,
    micgeom = micgeom,
    CSM = CSM,
    dr = true,
    flim = (800,4000),
    Nx = 61,
    Ny = 41,
    xlim = (-1.0,1.5),
    ylim = (-1.0,1.0)
)

# Now, we need to assign steering vectors (transfer functions) between the grid points defined in the environment `E` 
# and the microphone locations in `micgeom`, this is done in a simple manner:
steeringvectors!(E)
# where the "!" mutates the environment `E` and stores the steering vectors associated with the Environment. 
# If a flow field is defined in the environment, the correct steering vectors will automatically be calculated.

# Next, we calculate the beamforming image:
b = beamforming(E)
# the output is a `FreqArray` of size `E.Nx*E.Ny` times the number of frequency bins within the limits defined in `E`. 
# To plot the acoustic image, reshape the beamforming result, select a frequency bin and convert to dB:
fc = 2000
f_idx =  argmin(abs.(E.fn .- fc)) # finds index in E.fn that is closest to fc
bdB = SPL.(reshape(b[:,f_idx],E.Nx,E.Ny)) # conversion to dB.
maxdb = maximum(filter(!isnan,bdB)) # find peak dB value
dynrange = 12 # set beamforming dynamic range

# Now plot:
heatmap(E.rx,E.ry,bdB',clims=(maxdb-dynrange,maxdb),legend=false,cbar=true)
plot!([0.05,0.05],[-1,1],color="magenta") # Trailing edge position
x1,x2,y1,y2 = int_region
plot!([x1,x2,x2,x1,x1],[y1,y1,y2,y2,y1],color="magenta")
xlabel!("x [m]")
ylabel!("y [m]")
title!("NACA63018, no flow correction, freq = $(fc) Hz")
#savefig("no_flow_corr.png") # save like this
# Define a new Environment with shear layer correction:
E_flow = Environment(
    z0 = z0,
    micgeom = micgeom,
    CSM = CSM,
    dr = true,
    flim = (800,4000),
    Nx = 61,
    Ny = 41,
    xlim = (-1.0,1.5),
    ylim = (-1.0,1.0),
    # adding flow-info:
    shear = true,
    ampcorr = false,
    Ma = 0.24, # info from measurement
    h = 1.5, # distance from source to shear-layer plane
)

# Now, we need to assign steering vectors to the environment with a flow correction.
steeringvectors!(E_flow)
# Next, we calculate the new (flow-corrected) beamforming image:
b_flow = beamforming(E_flow)
fc = 2000
f_idx =  argmin(abs.(E_flow.fn .- fc)) # finds index in E.fn that is closest to fc
bdB_flow = SPL.(reshape(b_flow[:,f_idx],E_flow.Nx,E_flow.Ny)) # convertion to dB.
maxdb = maximum(filter(!isnan,bdB_flow)) # find peak dB value
dynrange = 12 # set beamforming dynamic range

# Now plot again:
heatmap(E_flow.rx,E_flow.ry,bdB_flow',clims=(maxdb-dynrange,maxdb),legend=false,cbar=true)
plot!([0.05,0.05],[-1,1],color="magenta") # Trailing edge position
x1,x2,y1,y2 = int_region
plot!([x1,x2,x2,x1,x1],[y1,y1,y2,y2,y1],color="magenta")
xlabel!("x [m]")
ylabel!("y [m]")
title!("NACA63018, with flow correction, freq = $(fc) Hz")
#savefig("flow_corr.png") # save like this
# Source integration
SPI_srcint = SPI(b,E,dxdy,int_region)
SPI_srcint_flow = SPI(b_flow,E_flow,dxdy,int_region)

plot(SPI_srcint.fc,SPL.(SPI_srcint),label="No flow correction",xscale=:log10,minorgrid=true,legend= :bottomleft,xticks=(1000:1000:4000, 1000:1000:4000))
plot!(SPI_srcint_flow.fc,SPL.(SPI_srcint_flow),label="With flow correction",xscale=:log10,minorgrid=true)
xlabel!("Frequency [Hz]")
ylabel!("Integrated spectrum [dB]")
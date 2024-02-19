ξ(Ma,a,b) = sqrt((1-Ma*a*b)^2-a^2)

function f!(F,x,Δxm,Δz2,Δz3,Ma,Δy)
    if (-0.8<=x[1]<=0.8) #&& (0.2<=abs(x[2])<=1)
        # change according to your implementation...
        Δx20 = Δz2 * x[1]*x[2]/ξ(Ma,x[1],x[2])
        Δx21 = Δz2 * Ma*(1-Ma*x[1]*x[2])/ξ(Ma,x[1],x[2])
        Δx3  = Δz3 * x[1]*x[2]/sqrt(1-x[1]^2)
        F[1] = Δx20 + Δx21 + Δx3 - Δxm
        F[2] = x[2] - (Δxm - Δx21)/sqrt((Δxm-Δx21)^2+Δy^2)
        return nothing
    else
        return nothing
    end
end

function my_custom_refraction_correction(Δx,Δy,Δz,Ma,h1,h2)
    r0 = sqrt(Δx^2+Δy^2+Δz^2)
    a0 = sqrt(Δx^2+Δy^2)/r0
    b0 = Δx/sqrt(Δx^2+Δy^2)
    Δz2,Δz3 = h1,h2
    
    res = nlsolve((F,x)->f!(F,x,Δx,Δz2,Δz3,Ma,Δy),[a0,b0],autoscale=false)
    a,b = res.zero
    
    r = ... # your implementation here

    return r
end

function my_custom_refraction_correction(E,h1=1.5,h2=E.z0-h1)
    @unpack M,N,Ma,Rxy,micgeom = E
    r = zeros(N,M)
    for n = 1:N
        for m = 1:M
            Δx,Δy,Δz = Rxy[:,n]-micgeom[:,m] # vector from mic to grid point
            r[n,m] = my_custom_refraction_correction(Δx,Δy,Δz,Ma,h1,h2)
        end
    end
    return r
end

function my_custom_steeringvectors!(E::Environment;multi_thread=E.multi_thread)
    _foreach = AeroAcoustics.check_multithread(multi_thread)
    @unpack fn,c,M,N,Nf,D,D0,Ma,h = E
    vi = Array{ComplexF64,3}(undef,N,M,Nf)
    w = 2pi*fn
    dx = my_custom_refraction_correction(E,h)
    ta = dx./c
    @views @inbounds _foreach(1:Nf) do j
        # your implementation below....
        vi[:,:,j] .= 1 ./(ta.*c.*D0.*sum(1 ./(ta.*c).^2,dims=2)).*exp.(-im.*w[j].*ta)
    end
    E.steeringvec = FreqArray(permutedims(vi,(2,1,3)),fn)
    return nothing
end